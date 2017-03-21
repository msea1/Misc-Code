import asyncio.subprocess 
 
 
async def get_date(): 
    code = 'ls -al /home/mcarruth/Code/block2/cmdseq-service/*.*' 
 
    # Create the subprocess, redirect the standard output into a pipe 
    create = asyncio.create_subprocess_shell(code, stdout=asyncio.subprocess.PIPE) 
    proc = await create 
 
    # Read one line of output 
    files = await proc.stdout.read() 
    line = files.decode('ascii').rstrip() 
 
    # Wait for the subprocess exit 
    await proc.wait() 
    return line 
 
loop = asyncio.get_event_loop() 
date = loop.run_until_complete(get_date()) 
print(date) 
loop.close() 

