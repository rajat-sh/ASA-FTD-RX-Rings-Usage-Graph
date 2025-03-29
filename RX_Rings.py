import matplotlib.pyplot as plt


def process_blocks_in_file(file_path):
    start_marker = "Interface Internal-Data0"
    end_marker = "Control Point Interface States:"
    
    inside_range = False
    blocks_data = []  # Store unique lists for each block
    interface_data_lists = []  # Lists for lines containing "RX" and not ": 0 packets, 0 bytes"
    error_lists = []  # Store error lists for each block

    # Open the file for reading
    try:
        with open(file_path, 'r') as file:
            current_block = []
            current_interface_data = []
            current_error_list = []
            contains_rx = False
            
            for line in file:
                # Check for the start marker
                if start_marker in line:
                    inside_range = True
                    current_block = []
                    current_interface_data = []
                    current_error_list = []
                    contains_rx = False
                    continue
                
                # Check for the end marker
                if end_marker in line:
                    inside_range = False
                    if contains_rx and current_block:
                        if current_block not in blocks_data:
                            blocks_data.append(current_block)
                            interface_data_lists.append(current_interface_data)
                            error_lists.append(current_error_list)
                    continue
                
                # Process lines within the block
                if inside_range:
                    current_block.append(line.strip())
                    if "RX" in line:
                        contains_rx = True
                        if ": 0 packets, 0 bytes" not in line:
                            current_interface_data.append(line.strip())
                    if "no buffer" in line or "input errors" in line:
                        current_error_list.append(line.strip())

        # Task 1: Error list processing
        for i, error_list in enumerate(error_lists, start=1):
            #print(f"Int_Error{i}:")
            concatenated_list = []
            for item in error_list:
                #print(item)
                split_items = item.split()  # Split each line on space boundaries
                concatenated_list.extend(split_items)
            #print()

            # Print the concatenated lists and specific elements with percentages
            #print(f"Concatenated_Int_Error{i}:")
            #print(concatenated_list)
            if len(concatenated_list) > 15:
                try:
                    packets_input = int(concatenated_list[0])
                    no_buffer = int(concatenated_list[5])
                    overruns = int(concatenated_list[15])

                    print(f"Packets_Input: {packets_input}")
                    print(f"No Buffer: {no_buffer}")
                    print(f"Overruns: {overruns}")

                    # Calculate percentages
                    no_buffer_percentage = (no_buffer / packets_input) * 100 if packets_input != 0 else 0
                    overruns_percentage = (overruns / packets_input) * 100 if packets_input != 0 else 0

                    print(f"No Buffer Percentage: {no_buffer_percentage:.2f}%")
                    print(f"Overruns Percentage: {overruns_percentage:.2f}%")
                except ValueError:
                    print("Non-numeric values encountered; unable to calculate percentages.")
            else:
                print("Not enough elements for Packet Input, No Buffer, and Overruns.")
            print()

        # Task 2: Interface data processing
        for i, interface_data in enumerate(interface_data_lists, start=1):
            modified_block = []
            #print(f"Interface_data_{i}:")
            for line in interface_data:
                line = line.replace(":", "", 1)
                if "packets," in line:
                    line = line.split("packets,", 1)[0].strip()
                elif "Packets:" in line:
                    line = line.replace("Packets:", "").split(" Bytes:", 1)[0].strip()
                modified_block.append(line)
                #print(line)
            #print()

            # Split elements with spaces into separate elements
            split_block = []
            for element in modified_block:
                if ' ' in element:
                    split_block.extend(element.split())
                else:
                    split_block.append(element)

            #print(f"Split_Interface_data_{i}:")
            #for item in split_block:
                #print(item)
            #print()

            # Calculate the sum of every second element in the split list
            Total_Packets = 0
            for j in range(1, len(split_block), 2):
                try:
                    Total_Packets += int(split_block[j])
                except ValueError:
                    print(f"Skipping non-numeric value: {split_block[j]}")

            #print(f"Total_Packets_{i}: {Total_Packets}")

            # Create a list of every first, third, fifth element, etc.
            RX_Num = split_block[::2]
            #print(f"RX_Num_{i}:")
            #for element in RX_Num:
                #print(element)
            #print()

            # Calculate the percentage of every second item with respect to Total_Packets
            RX_Percentages = []
            for j in range(1, len(split_block), 2):
                try:
                    value = int(split_block[j])
                    percentage = (value / Total_Packets) * 100 if Total_Packets != 0 else 0
                    RX_Percentages.append(percentage)
                except ValueError:
                    print(f"Skipping non-numeric value: {split_block[j]}")

            #print(f"RX_Percentages_{i}:")
            #for percentage in RX_Percentages:
                #print(f"{percentage:.2f}%")
            #print()

            # Create a bar graph using RX_Num and RX_Percentages
            plt.figure(figsize=(10, 6))
            plt.bar(RX_Num, RX_Percentages, color='blue')
            plt.xlabel('RX_Num')
            plt.ylabel('RX_Percentages')
            plt.title(f'RX Percentages Bar Graph for Block {i}')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
file_path = input("Please enter the file path: ")
process_blocks_in_file(file_path)
