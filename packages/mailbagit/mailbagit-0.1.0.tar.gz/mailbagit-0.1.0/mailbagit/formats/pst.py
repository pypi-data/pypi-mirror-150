import os
import mailbox
from pathlib import Path
import chardet
from extract_msg.constants import CODE_PAGES
from structlog import get_logger
from email import parser
from mailbagit.email_account import EmailAccount
from mailbagit.models import Email, Attachment
import mailbagit.helper as helper

# only create format if pypff is successfully importable -
# pst is not supported otherwise
skip_registry = False
try:
    import pypff
except:
    skip_registry = True

log = get_logger()

if not skip_registry:

    class PST(EmailAccount):
        # pst - This concrete class parses PST file format
        format_name = "pst"
        try:
            from importlib import metadata
        except ImportError:  # for Python<3.8
            import importlib_metadata as metadata
        format_agent = pypff.__name__
        format_agent_version = metadata.version("libpff-python")

        def __init__(self, target_account, args, **kwargs):
            log.debug("Parsity parse")
            # code goes here to set up mailbox and pull out any relevant account_data

            self.path = target_account
            self.dry_run = args.dry_run
            self.mailbag_name = args.mailbag_name
            self.iteration_only = False
            log.info("Reading :", Path=self.path)

        def account_data(self):
            return account_data

        def folders(self, folder, path, originalFile):
            # recursive function that calls itself on any subfolders and
            # returns a generator of messages
            # path is a list that you can create the filepath with os.path.join()
            if folder.number_of_sub_messages:
                log.debug("Reading folder: " + folder.name)
                path.append(folder.name)
                for index in range(folder.number_of_sub_messages):

                    if self.iteration_only:
                        yield None
                        continue
                    attachments = []
                    errors = {}
                    errors["msg"] = []
                    errors["stack_trace"] = []
                    try:
                        messageObj = folder.get_sub_message(index)

                        try:
                            headerParser = parser.HeaderParser()
                            headers = headerParser.parsestr(messageObj.transport_headers)
                        except Exception as e:
                            desc = "Error parsing message body"
                            errors = helper.handle_error(errors, e, desc)

                        try:
                            # Parse message bodies
                            html_body = None
                            text_body = None
                            html_encoding = None
                            text_encoding = None

                            # Codepage integers found here: https://github.com/libyal/libpff/blob/main/libpff/libpff_mapi.h#L333-L335
                            # Docs say to use MESSAGE_CODEPAGE: https://github.com/libyal/libfmapi/blob/main/documentation/MAPI%20definitions.asciidoc#51-the-message-body
                            # this is a 32bit encoded integer
                            encodings = {}
                            LIBPFF_ENTRY_TYPE_MESSAGE_BODY_CODEPAGE = int("0x3fde", base=16)
                            LIBPFF_ENTRY_TYPE_MESSAGE_CODEPAGE = int("0x3ffd", base=16)
                            for record_set in messageObj.record_sets:
                                for entry in record_set.entries:
                                    if entry.entry_type == LIBPFF_ENTRY_TYPE_MESSAGE_BODY_CODEPAGE:
                                        if entry.data:
                                            value = entry.get_data_as_integer()
                                            # Use the extract_msg code page in constants.py
                                            encodings["PidTagInternetCodepage"] = CODE_PAGES[value]
                                    if entry.entry_type == LIBPFF_ENTRY_TYPE_MESSAGE_CODEPAGE:
                                        if entry.data:
                                            value = entry.get_data_as_integer()
                                            # Use the extract_msg code page in constants.py
                                            encodings["PidTagMessageCodepage"] = CODE_PAGES[value]

                            if messageObj.html_body:
                                if encodings["PidTagInternetCodepage"]:
                                    html_encoding = encodings["PidTagInternetCodepage"]
                                elif encodings["PidTagMessageCodepage"]:
                                    html_encoding = encodings["PidTagMessageCodepage"]
                                else:
                                    html_encoding = chardet.detect(messageObj.html_body)["encoding"]
                                html_body = messageObj.html_body.decode(html_encoding)
                            if messageObj.plain_text_body:
                                if encodings["PidTagInternetCodepage"]:
                                    text_encoding = encodings["PidTagInternetCodepage"]
                                elif encodings["PidTagMessageCodepage"]:
                                    text_encoding = encodings["PidTagMessageCodepage"]
                                else:
                                    text_encoding = chardet.detect(messageObj.plain_text_body)["encoding"]
                                text_encoding = chardet.detect(messageObj.plain_text_body)["encoding"]
                                text_body = messageObj.plain_text_body.decode(text_encoding)

                        except Exception as e:
                            desc = "Error parsing message body"
                            errors = helper.handle_error(errors, e, desc)

                        # Build message and derivatives paths
                        try:
                            messagePath = os.path.join(os.path.splitext(originalFile)[0], *path)
                            if len(messagePath) > 0:
                                messagePath = Path(messagePath).as_posix()
                            derivativesPath = helper.normalizePath(messagePath)
                        except Exception as e:
                            desc = "Error reading message path"
                            errors = helper.handle_error(errors, e, desc)

                        try:
                            total_attachment_size_bytes = 0
                            for attachmentObj in messageObj.attachments:
                                total_attachment_size_bytes = total_attachment_size_bytes + attachmentObj.get_size()
                                attachment_content = attachmentObj.read_buffer(attachmentObj.get_size())

                                try:
                                    # attachmentName = attachmentObj.get_name()
                                    # Entries found here: https://github.com/libyal/libpff/blob/main/libpff/libpff_mapi.h#L333-L335
                                    LIBPFF_ENTRY_TYPE_ATTACHMENT_FILENAME_LONG = int("0x3707", base=16)
                                    LIBPFF_ENTRY_TYPE_ATTACHMENT_FILENAME_SHORT = int("0x3704", base=16)
                                    LIBPFF_ENTRY_TYPE_ATTACHMENT_MIME_TAG = int("0x370e", base=16)
                                    attachmentLong = ""
                                    attachmentShort = ""
                                    mime = None
                                    for record_set in attachmentObj.record_sets:
                                        for entry in record_set.entries:
                                            if entry.entry_type == LIBPFF_ENTRY_TYPE_ATTACHMENT_FILENAME_LONG:
                                                if entry.data:
                                                    attachmentLong = entry.get_data_as_string()
                                            if entry.entry_type == LIBPFF_ENTRY_TYPE_ATTACHMENT_FILENAME_SHORT:
                                                if entry.data:
                                                    attachmentShort = entry.get_data_as_string()
                                            if entry.entry_type == LIBPFF_ENTRY_TYPE_ATTACHMENT_MIME_TAG:
                                                if entry.data:
                                                    mime = entry.get_data_as_string()
                                    # Use the Long filename preferably
                                    if len(attachmentLong) > 0:
                                        attachmentName = attachmentLong
                                    elif len(attachmentShort) > 0:
                                        attachmentName = attachmentShort
                                    else:
                                        print(message.Mailbag_Message_ID)
                                        raise ValueError("No attachment name found.")

                                    # Guess the mime if we can't find it
                                    if mime is None:
                                        mime = helper.guessMimeType(attachmentName)

                                except Exception as e:
                                    attachmentName = str(len(attachments))
                                    desc = (
                                        "No filename found for attachment "
                                        + attachmentName
                                        + " for message "
                                        + str(message.Mailbag_Message_ID)
                                    )
                                    errors = helper.handle_error(errors, e, desc)

                                attachment = Attachment(
                                    Name=attachmentName,
                                    File=attachment_content,
                                    MimeType=mime,
                                )
                                attachments.append(attachment)

                        except Exception as e:
                            desc = "Error parsing attachments"
                            errors = helper.handle_error(errors, e, desc)

                        message = Email(
                            Error=errors["msg"],
                            Message_ID=helper.parse_header(headers["Message-ID"]),
                            Original_File=originalFile,
                            Message_Path=messagePath,
                            Derivatives_Path=derivativesPath,
                            Date=helper.parse_header(headers["Date"]),
                            From=helper.parse_header(headers["From"]),
                            To=helper.parse_header(headers["To"]),
                            Cc=helper.parse_header(headers["Cc"]),
                            Bcc=helper.parse_header(headers["Bcc"]),
                            Subject=helper.parse_header(headers["Subject"]),
                            Content_Type=headers.get_content_type(),
                            Headers=headers,
                            HTML_Body=html_body,
                            HTML_Encoding=html_encoding,
                            Text_Body=text_body,
                            Text_Encoding=text_encoding,
                            Message=None,
                            Attachments=attachments,
                            StackTrace=errors["stack_trace"],
                        )

                    except (Exception) as e:
                        desc = "Error parsing message"
                        errors = helper.handle_error(errors, e, desc)
                        message = Email(Error=errors["msg"], StackTrace=errors["stack_trace"])

                    yield message

            # iterate over any subfolders too
            if folder.number_of_sub_folders:
                for folder_index in range(folder.number_of_sub_folders):
                    subfolder = folder.get_sub_folder(folder_index)
                    yield from self.folders(subfolder, path, originalFile)
            else:
                # gotta return empty directory to controller somehow
                log.warn("Empty folder " + folder.name + " not handled.")

        def messages(self):
            if os.path.isfile(self.path):
                parent_dir = os.path.dirname(self.path)
                fileList = [self.path]
            else:
                parent_dir = self.path
                fileList = []
                for root, dirs, files in os.walk(self.path):
                    for file in files:
                        if file.lower().endswith("." + self.format_name):
                            fileList.append(os.path.join(root, file))

            for filePath in fileList:
                originalFile = helper.relativePath(self.path, filePath)
                if len(originalFile) < 1:
                    pathList = []
                else:
                    pathList = os.path.normpath(originalFile).split(os.sep)

                pst = pypff.file()
                pst.open(filePath)
                root = pst.get_root_folder()
                for folder in root.sub_folders:
                    if folder.number_of_sub_folders:
                        # call recursive function to parse email folder
                        yield from self.folders(folder, pathList, os.path.basename(filePath))
                    else:
                        # gotta return empty directory to controller somehow
                        log.warn("Empty folder " + folder.name + " not handled.")
                pst.close()

                # Move PST to new mailbag directory structure
                if not self.iteration_only:
                    new_path = helper.moveWithDirectoryStructure(
                        self.dry_run,
                        parent_dir,
                        self.mailbag_name,
                        self.format_name,
                        filePath,
                    )
