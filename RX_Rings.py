import chardet
import matplotlib.pyplot as plt

def detect_file_encoding(file_path):
    """Detects file encoding by reading a portion of the file."""
    with open(file_path, 'rb') as file:
        raw_data = file.read(10000)  # Read first 10000 bytes
    return chardet.detect(raw_data)['encoding']

def process_blocks_in_file(file_path):
    """Processes blocks of lines in a file based on specified markers."""
    # Detect file encoding
    encoding = detect_file_encoding(file_path)
    #print(f"Detected file encoding: {encoding}")

    start_marker = "Interface Internal-Data0"
    end_marker = "Control Point Interface States:"
    
    inside_range = False
    blocks_data = []  # Store unique lists for each block
    error_lists = []  # Store error lists for each block
    freeblock_data_lists = []  # Store RX data lists for each block
    interface_data_lists = []  # Store RX interface data for each block

    # Open the file for reading with detected encoding
    try:
        with open(file_path, 'r', encoding=encoding) as file:
            current_block = []
            current_error_list = []
            current_rx_data = []
            current_interface_data = []
            contains_rx = False
            
            for line in file:
                # Check for the start marker
                if start_marker in line:
                    inside_range = True
                    current_block = []
                    current_error_list = []
                    current_rx_data = []
                    current_interface_data = []
                    contains_rx = False
                    continue

                # Check for the end marker
                if end_marker in line:
                    inside_range = False
                    if contains_rx and current_block not in blocks_data:  # Check for uniqueness
                        blocks_data.append(current_block)
                        error_lists.append(current_error_list)
                        freeblock_data_lists.append(current_rx_data)
                        interface_data_lists.append(current_interface_data)
                    continue

                # Process lines within the block
                if inside_range:
                    stripped_line = line.strip()
                    if stripped_line:
                        current_block.append(stripped_line)
                        if "RX" in stripped_line and ": 0 packets, 0 bytes" not in stripped_line:
                            contains_rx = True
                            current_rx_data.append(stripped_line)
                            current_interface_data.append(stripped_line)
                            # Also add the next line if available
                            next_line = next(file, None)
                            if next_line:
                                current_rx_data.append(next_line.strip())
                                current_interface_data.append(next_line.strip())
                    if "no buffer" in stripped_line or "input errors" in stripped_line:
                        current_error_list.append(stripped_line)

        # Process and print error lists and their split versions
        for i, error_list in enumerate(error_lists, start=1):
            #print(f"Int_Error{i}:")
            concatenated_list = []
            for item in error_list:
                #print(item)
                split_items = item.split()  # Split each line on space boundaries
                concatenated_list.extend(split_items)
            #print(f"Concatenated_Int_Error{i}: {concatenated_list}")

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
            print()  # Newline for separation between concatenated lists

        # Process Freeblock_data lists containing RX-related information
        for i, freeblock_data in enumerate(freeblock_data_lists, start=1):
            #print(f"Freeblock_data_{i}:")
            split_data = []
            for item in freeblock_data:
                split_items = item.split()  # Split on space boundaries
                split_data.extend(split_items)
            #print(f"Split Freeblock_data_{i}: {split_data}")

            # Filter and print elements containing "RX" or "/"
            filtered_data = [value for value in split_data if "RX" in value or "/" in value]
            #print(f"Filtered Freeblock_data_{i}: {filtered_data}")

            # Split filtered data on "/"
            split_filtered_data = [part for value in filtered_data for part in value.split("/")]
            #print(f"Split Filtered Freeblock_data_{i}: {split_filtered_data}")

            # Check for values less than 10 and print accordingly
            print("Potential RX rings with Current or Previous Low Blocks for Interface Block Number",i,",low Blocks threshold is 10:")
            for j in range(0, len(split_filtered_data), 5):
                if j+4 < len(split_filtered_data) and (
                        (split_filtered_data[j+3].isdigit() and int(split_filtered_data[j+3]) < 10) or
                        (split_filtered_data[j+4].isdigit() and int(split_filtered_data[j+4]) < 10)):
                    print(" ".join(split_filtered_data[j:j+5]))
            print()  # Newline for separation

        # Process and print Interface_data lists
        for i, interface_data in enumerate(interface_data_lists, start=1):
            #print(f"Interface_data_{i}:")
            split_interface_data = []
            rx_elements = []
            packets_elements = []

            for item in interface_data:
                #print(item)
                split_items = item.split()  # Split each line on space boundaries
                split_interface_data.extend(split_items)
                for idx, element in enumerate(split_items):
                    if element == "packets," and idx > 0:
                        packets_elements.append(split_items[idx - 1])
                    elif element == "Packets:" and idx < len(split_items) - 1:
                        packets_elements.append(split_items[idx + 1])
                    if "RX" in element:
                        rx_elements.append(element)

            # Determine which case to execute based on presence of "packets,"
            rx_interface_data = packets_elements

            # Calculate Total_Packets if there are at least two elements
            total_packets = sum(int(e) for e in rx_interface_data if e.isdigit())
            #if len(rx_interface_data) >= 2:
                #print(f"RX_Interface_data_{i}: {rx_interface_data}")
                #print(f"Total_Packets_{i}: {total_packets}")
            #else:
                #print(f"RX_Interface_data_{i} is too small for calculation.")

            #print(f"RXNUMInterface_data_{i}: {rx_elements}")

            # Calculate RX_Percentages
            rx_percentages = [(int(e) / total_packets) * 100 if total_packets != 0 else 0 for e in rx_interface_data if e.isdigit()]
            #print(f"RX_Percentages_{i}: {rx_percentages}")

            # Create bar graph
            plt.figure(figsize=(10, 6))
            plt.bar(rx_elements, rx_percentages, color='blue')
            plt.xlabel(f'RXInterface_data_{i}')
            plt.ylabel('RX_Percentages')
            plt.title(f'RX Data Analysis for Interface_Block{i}')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()

            print()  # Newline for separation

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    file_path = input("Please enter the path to the file: ")
    process_blocks_in_file(file_path)

if __name__ == "__main__":
    main()
