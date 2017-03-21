
# return codes from asyncio are negative
SIGINT = -2
SIGKILL = -9
SIGTERM = -15


def was_proc_cancelled(exit_code):
    return exit_code in [SIGINT, SIGKILL, SIGTERM]


def get_proc_exit_code(proc):
    if not proc:
        return None
    return proc.returncode


async def list_files_long(cmdseq, cmd_obj):
    sc_file_type = ScFileType[cmd_obj.Args['sc_file_type']]
    file_path = FILE_PATHS[sc_file_type.name]
    cmd = f"ls -al {file_path}*.{FILE_EXTENSIONS[sc_file_type.name]}"  # ex: ls -al /var/imgs/*.img
    ls_proc = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE)
    # file_type = FILE_EXTENSIONS[sc_file_type.name]
    # path = os.path.join(file_path, f'*.{file_type}')
    # files = glob.glob(path)  # TODO also get md5 and other assorted info?
    files = await ls_proc.stdout.read()
    output = files.decode('ascii').rstrip()
    await ls_proc.wait()
    exit_code = get_proc_exit_code(ls_proc)
    if exit_code == 0:
        return output
    elif was_proc_cancelled(exit_code):
        raise CommandSequenceError(f"Listing {sc_file_type.name} files at {file_path} cancelled")
    else:
        raise CommandSequenceError(f"Listing {sc_file_type.name} files at {file_path} failed with exit code {exit_code}")
    return str(files)


async def list_files(cmdseq, cmd_obj):
    sc_file_type = ScFileType[cmd_obj.Args['sc_file_type']]
    file_path = FILE_PATHS[sc_file_type.name]
    file_type = FILE_EXTENSIONS[sc_file_type.name]
    path = os.path.join(file_path, f'*.{file_type}')
    files = glob.glob(path)
    return str(files)


async def delete_file_long(cmdseq, cmd_obj):
    file_path = cmd_obj.Args['file_path']
    if not os.path.isfile(file_path):
        raise CommandSequenceError(f"Deleting {file_path} failed because no file found.")
    # os.remove(file_path)
    cmd = f"rm {file_path}"
    rm_proc = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE)
    await rm_proc.wait()
    exit_code = get_proc_exit_code(rm_proc)
    if exit_code == 0:
        return f"{file_path} deleted"
    elif was_proc_cancelled(exit_code):
        raise CommandSequenceError(f"Deleting {file_path} cancelled")
    else:
        raise CommandSequenceError(f"Deleting {file_path} failed with exit code {exit_code}")
    return f"{file_path} deleted"


async def delete_file(cmdseq, cmd_obj):
    file_path = cmd_obj.Args['file_path']
    if not os.path.isfile(file_path):
        raise CommandSequenceError(f"Deleting {file_path} failed because no file found.")
    os.remove(file_path)
    return f"{file_path} deleted"
