_ = """ 2024/03/18
Status modification of the added data points:
> It is possible to disable/enable a data point; a disabled data point will not be measured;
> It is possible to modify the description information of data points;

Front-end and back-end interaction modification:
> Use WebSocket to update the state description of data points, it will not timeout easily anymore;
> Use WebSocket for status update during running process to ease the waiting anxiety;
"""

_032178 = """ 2024/02/25
Protect source code files with a password (Go to "Settings" to view):
>  Upload the zip file encrypted in bytes;
>  Encrypt the key randomly and upload it;
>  Delete the source code once the server has finished compiling, keeping only the zip encrypted by the key;

Show updates:
>  Show update after update as you have seen so far;
"""

_032026 = """ 2024/02/24
Optimise the usage experience:
>  Data is now automatically synchronised after submitting code or uploading data;
>  Syncing data doesn't force to jump to the latest unit anymore;

UI design optimisation:
>  Adjusted the component hierarchy of the main interface to eliminate potential code warnings;

Robustness improvement:
>  Special handling for empty paths;
"""

_021946 = """ 2024/02/24
First release!
"""

ChangeLog = {
    "032178": _032178,
    "032026": _032026,
    "021946": _021946
}
