import subprocess
import pandas as pd
from kthread_sleep import sleep
from subprocesskiller import kill_subprocs
from io import StringIO
import numpy as np
from getfilenuitkapython import get_filepath
import ctypes
from ctypes import wintypes

handle = get_filepath("handle.exe")


def get_handle_df_with_address() -> pd.DataFrame:
    r"""
           HandleType  Flags  HandleNumber  KernelAddress  GrantedAccess  PID Process                  User      Handle       Type ShareFlags                     Name                                                                AccessMask
    0           7      0             4   1.844663e+19        2097151    4  System  \NT AUTHORITY\SYSTEM  0x00000004    Process             <Error Opening Process>  READ_CONTROL|DELETE|SYNCHRONIZE|WRITE_DAC|WRITE_OWNER|PROCESS_ALL_ACCESS
    1           8      0             8   1.844663e+19        2097151    4  System  \NT AUTHORITY\SYSTEM  0x00000008     Thread              <Error Opening Thread>   READ_CONTROL|DELETE|SYNCHRONIZE|WRITE_DAC|WRITE_OWNER|THREAD_ALL_ACCESS
    2          44      0            12   1.844668e+19             16    4  System  \NT AUTHORITY\SYSTEM  0x0000000C        Key                                 NaN                                                                    NOTIFY
    3          17      0            16   1.844663e+19        2031617    4  System  \NT AUTHORITY\SYSTEM  0x00000010     Mutant                                 NaN   READ_CONTROL|DELETE|SYNCHRONIZE|WRITE_DAC|WRITE_OWNER|MUTANT_ALL_ACCESS
    4           3      0            20   1.844668e+19         983055    4  System  \NT AUTHORITY\SYSTEM  0x00000014  Directory                                 NaN            READ_CONTROL|DELETE|WRITE_DAC|WRITE_OWNER|DIRECTORY_ALL_ACCESS
    """
    SystemHandleInformation = 16
    STATUS_BUFFER_TOO_SMALL = 0xC0000023
    STATUS_SUCCESS = 0x00000000
    PVOID = ctypes.c_void_p

    class SYSTEM_HANDLE(ctypes.Structure):
        _fields_ = [
            ("ProcessId", wintypes.ULONG),
            ("HandleType", wintypes.BYTE),
            ("Flags", wintypes.BYTE),
            ("HandleNumber", wintypes.SHORT),
            ("KernelAddress", PVOID),
            ("GrantedAccess", wintypes.ULONG),
        ]

    class SYSTEM_HANDLE_INFORMATION(ctypes.Structure):
        _fields_ = [
            ("NumberOfHandles", wintypes.ULONG),
            ("Handles", SYSTEM_HANDLE * 10000000),
        ]

    ntdll = ctypes.WinDLL("ntdll")
    ntdll.NtQuerySystemInformation.argtypes = [
        wintypes.ULONG,
        ctypes.POINTER(SYSTEM_HANDLE_INFORMATION),
        wintypes.ULONG,
        ctypes.POINTER(wintypes.ULONG),
    ]

    handle_info_size = wintypes.ULONG()
    ntdll.NtQuerySystemInformation(
        SystemHandleInformation, None, 0, ctypes.byref(handle_info_size)
    )

    buffer_size = handle_info_size.value
    buffer = ctypes.create_string_buffer(buffer_size)
    handle_info = ctypes.cast(buffer, ctypes.POINTER(SYSTEM_HANDLE_INFORMATION))

    while True:
        status = ntdll.NtQuerySystemInformation(
            SystemHandleInformation,
            handle_info,
            buffer_size,
            ctypes.byref(handle_info_size),
        )
        if status == STATUS_SUCCESS:
            break
        elif status == STATUS_BUFFER_TOO_SMALL or handle_info_size.value > buffer_size:
            buffer_size = handle_info_size.value
            buffer = ctypes.create_string_buffer(buffer_size)
            handle_info = ctypes.cast(buffer, ctypes.POINTER(SYSTEM_HANDLE_INFORMATION))
        else:
            raise RuntimeError("NtQuerySystemInformation failed")
    alla = []
    for i in range(handle_info.contents.NumberOfHandles):
        try:
            handle = handle_info.contents.Handles[i]  # .HandleNumber
            alla.append(
                (
                    handle.ProcessId,
                    handle.HandleType,
                    handle.Flags,
                    handle.HandleNumber,
                    handle.KernelAddress,
                    handle.GrantedAccess,
                )
            )
        except Exception as fe:
            continue
    df = pd.DataFrame(
        alla,
        columns=[
            "ProcessId",
            "HandleType",
            "Flags",
            "HandleNumber",
            "KernelAddress",
            "GrantedAccess",
        ],
    )
    df3 = get_handle_list(partial_process_string="")
    df3["HandleNumber"] = df3.Handle.apply(lambda x: int(x, base=16)).astype("Int64")
    df["HandleNumber"] = df["HandleNumber"].astype("Int64")
    df["PID"] = df["ProcessId"].astype("Int64")
    df3["PID"] = df3["PID"].astype("Int64")
    df = pd.merge(df, df3, how="outer")
    df["HandleType"] = df["HandleType"].astype("Int64")
    df["Flags"] = df["Flags"].astype("Int64")
    df["GrantedAccess"] = df["GrantedAccess"].astype("Int64")
    df = df.drop(columns="ProcessId")  # .copy()
    df = df.loc[~df.HandleType.isna()].reset_index(drop=True)
    return df




def get_handle_list(partial_process_string: str = "") -> pd.DataFrame:
    r"""
    Retrieve the list of handles using the 'handle.exe' command and return the data as a pandas DataFrame.

    Args:
        partial_process_string (str): A partial process string to filter the handles by a specific process.
            Defaults to an empty string, which retrieves handles for all processes.

    Returns:
        pd.DataFrame: A DataFrame containing information about the handles.

    Raises:
        None

    Example:
        >>> df = get_handle_list(partial_process_string="explorer.exe")
        >>> print(df.head())
              Process  PID               User   Handle Type ShareFlags  \
        0  System         4  NT AUTHORITY\SYSTEM  0x3f4    Key
        1  System         4  NT AUTHORITY\SYSTEM  0x6cc    Key
        2  System         4  NT AUTHORITY\SYSTEM  0x78c    Key
        3  System         4  NT AUTHORITY\SYSTEM  0x790    Key
        4  System         4  NT AUTHORITY\SYSTEM  0x7a8    Key

                          Name            AccessMask
        0  \REGISTRY\MACHINE\BCD       0x20019
        1  \REGISTRY\MACHINE\BCD       0x20019
        2  \REGISTRY\MACHINE\BCD       0x20019
        3  \REGISTRY\MACHINE\BCD       0x20019
        4  \REGISTRY\MACHINE\BCD       0x20019
        ...
    """
    if partial_process_string:
        cm = [
            handle,
            "-accepteula",
            "-a",
            "-g",
            "-v",
            "-nobanner",
            "-p",
            str(partial_process_string),
        ]
    else:
        cm = [handle,"-accepteula", "-a", "-g", "-v", "-nobanner"]
    p = subprocess.run(cm, capture_output=True)
    csv_data = p.stdout.decode("utf-8", "ignore")
    csv_io = StringIO(csv_data)
    df = pd.read_csv(csv_io, encoding_errors="ignore", on_bad_lines="skip")

    df.columns = [
        "Process",
        "PID",
        "User",
        "Handle",
        "Type",
        "ShareFlags",
        "Name",
        "AccessMask",
    ]
    alldtypes = [
        ("Process", "category"),
        ("PID", np.uint16),
        ("User", "category"),
        ("Handle", "category"),
        ("Type", "category"),
        ("ShareFlags", "category"),
        ("Name", "category"),
        ("AccessMask", "category"),
    ]
    for key, cat in alldtypes:
        try:
            if key == "ShareFlags":
                df[key] = df[key].fillna("")
            df[key] = df[key].astype(cat)
        except Exception:
            pass

    return df


def get_handle_list_interval(interval:int=5, partial_process_string:str="")->pd.DataFrame:
    r"""
    Continuously retrieve the list of handles at a specified interval using the 'handle.exe' command
    and return the data as a concatenated pandas DataFrame. Press ctrl+c when you want the capturing to stop

    Args:
        interval (int): The interval in seconds at which to retrieve the handle list. Defaults to 5.
        partial_process_string (str): A partial process string to filter the handles by a specific process.
            Defaults to an empty string, which retrieves handles for all processes.

    Returns:
        pd.DataFrame: A DataFrame containing information about the handles.

    Raises:
        None

    Example:
        >>> df = get_handle_list_interval(interval=1, partial_process_string="")
        >>> print(df.head())
              Process  PID               User   Handle Type ShareFlags  \
        0  System         4  NT AUTHORITY\SYSTEM  0x3f4    Key
        1  System         4  NT AUTHORITY\SYSTEM  0x6cc    Key
        2  System         4  NT AUTHORITY\SYSTEM  0x78c    Key
        3  System         4  NT AUTHORITY\SYSTEM  0x790    Key
        4  System         4  NT AUTHORITY\SYSTEM  0x7a8    Key

                          Name            AccessMask  scan_id
        0  \REGISTRY\MACHINE\BCD       0x20019           0
        1  \REGISTRY\MACHINE\BCD       0x20019           0
        2  \REGISTRY\MACHINE\BCD       0x20019           0
        3  \REGISTRY\MACHINE\BCD       0x20019           0
        4  \REGISTRY\MACHINE\BCD       0x20019           0
        ...
    """
    alldfs = []
    scanid = 0
    try:
        while True:
            try:
                alldfs.append(
                    get_handle_list(
                        partial_process_string=partial_process_string
                    ).assign(scan_id=scanid)
                )
                scanid += 1

            except KeyboardInterrupt:
                print("Killing handle...")

                kill_subprocs(dontkill=(("Caption", "conhost.exe"),))
                print("Creating data frame...")
                sleep(2)
                break
            except Exception:
                pass
            sleep(interval)
    except KeyboardInterrupt:
        print("Killing handle...")

        kill_subprocs(dontkill=(("Caption", "conhost.exe"),))
        print("Creating data frame...")
        sleep(2)
    return pd.concat(alldfs, ignore_index=True)


# examples
# df = get_handle_list(partial_process_string="explorer.exe")
# df2 = get_handle_list_interval(interval=1, partial_process_string="")
# df3  = get_handle_df_with_address()