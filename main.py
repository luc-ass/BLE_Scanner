import asyncio
import argparse
from bleak import BleakScanner

async def main(target_mac=None):
    with open("ble_log.txt", "w") as log_file:
        def detection_callback(device, advertisement_data):
            mac_address = device.address.lower()  # MAC address of the device
            
            # Skip if we're looking for a specific MAC and this isn't it
            if target_mac and mac_address != target_mac.lower():
                return
                
            log_entry = (
                f"MAC Address: {mac_address}\n"
                f"Device Name: {device.name}\n"
                f"Advertisement Data: {advertisement_data}\n"
                "----------------------------------------\n"
            )
            print(log_entry)
            log_file.write(log_entry)

        scanner = BleakScanner(detection_callback)
        await scanner.start()
        
        if target_mac:
            print(f"Scanning for BLE device with MAC: {target_mac}...")
        else:
            print("Scanning for all BLE devices...")
            
        await asyncio.sleep(10.0)  # Adjust the duration as needed
        await scanner.stop()
        print("Scan completed.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='BLE Scanner')
    parser.add_argument('--mac', 
                       help='MAC address to filter (format: xx:xx:xx:xx:xx:xx)',
                       type=str,
                       required=False)
    
    args = parser.parse_args()
    
    # Validate MAC address format if provided
    if args.mac:
        # Simple validation of MAC address format
        if len(args.mac.replace(':', '')) != 12:
            print("Error: Invalid MAC address format. Use xx:xx:xx:xx:xx:xx")
            exit(1)
    
    asyncio.run(main(args.mac))
