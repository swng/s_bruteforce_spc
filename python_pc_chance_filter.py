import subprocess
import re

async def make_sys_call(command):
    process = await asyncio.create_subprocess_shell(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True
    )
    stdout, stderr = await process.communicate()
    if process.returncode != 0:
        print(f"Error executing command: {command}")
        print(f"Error message: {stderr.decode()}")
        return None
    return stdout.decode()

async def pc_chance_filter(fumen, missing_pieces):
    command = f"java -jar sfinder.jar percent -K +t -d 180 -p '[{missing_pieces}]!,*!' -t '{fumen}' -c 6"
    if len(missing_pieces) == 0:
        command = f"java -jar sfinder.jar percent -K +t -d 180 -p '*!' -t '{fumen}' -c 6"
    
    results_string = await make_sys_call(command)
    results_list = results_string.split("\n")
    
    for line in results_list:
        if "success" in line:
            line = line.replace(",", '.')  # for localization purposes
            percentage_match = re.search(r'(\d+\.\d+)%', line)
            
            if percentage_match and percentage_match.group(1):
                percentage_value = float(percentage_match.group(1))
                print(percentage_value)
                
                if percentage_value >= 98.0:
                    return percentage_value
    
    return 0.0

async def main():
    with open("./step_c_2.txt", 'r') as input_file, open("step_d.txt", 'w') as output_file:
        line_count = 0
        
        for line in input_file:
            line_count += 1
            
            if line_count >= 99869:
                print(f"Line {line_count}")
                
                split_line = line.strip().split(",")
                process_pc_chance = await pc_chance_filter(split_line[0], split_line[1])
                
                if (process_pc_chance >= 98.0 and len(split_line[1]) == 0) or \
                   (process_pc_chance >= 99.0 and len(split_line[1]) == 1) or \
                   process_pc_chance >= 100:
                    output_file.write(f"{process_pc_chance},{line}")
    
    print('Processing completed.')

# Import asyncio for the asynchronous operations
import asyncio

# Run the main function
asyncio.run(main())
