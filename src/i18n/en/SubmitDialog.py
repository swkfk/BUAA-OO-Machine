class Strings:
    class Window:
        Title = "Submit - {}"
        Wait = "Waiting for submission..."

    class Status:
        Zipping = "Archiving the sources..."
        Submitting = "Uploading..."
        Unzipping = "Unzipping..."
        Compiling = "Compiling..."
        Running = "Running..."
        Done = "Done！"

        Hint = [Submitting, Unzipping,  Compiling, Running, Done]

        CE_Title = "Compile Error!"
        RE_Title = "Runtime Error!"
        RE_Content = "At least one point occurred an exception! <br />"\
                     "Click the index label of each points (such as the <code>#0</code>) <br />" \
                     "to view the <code>RuntimeError</code> message."

    class Ask:
        Title = "Enter the Java Main Class, with the full package path"
        Confirm = "Confirm"
        Cancel = "Cancel"
        NoAskMore = "Confirm (Without Asking More)"
