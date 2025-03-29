Sometimes it is useful to see the load distribution across RX rings, uneven load may cause. packet drops.

 

Srcipt takes "show tech" as input. Example below, it will show the input packets, no buffer, overruns counts and percentages of internal-data interfaces in same order as they appear in show tech and it will plot graph was RX rings use percentages.

 

RAJATSH-M-V7QW:LIST_PYTHON rajatsh$ python3 RX_Rings.py

 

Please enter the file path: 27tech

Packets_Input: 1409805310570

No Buffer: 2624035938

Overruns: 0

No Buffer Percentage: 0.19%

Overruns Percentage: 0.00%

 

Packets_Input: 282562757349

No Buffer: 95407031

Overruns: 0

No Buffer Percentage: 0.03%

Overruns Percentage: 0.00%



 Normally in tickets like these next step would be to look as asp load balancing settings.

 

https://www.cisco.com/c/en/us/td/docs/security/asa/asa-cli-reference/A-H/asa-command-ref-A-H/ar-az-c...

 

 

Please note:

 

For some input files i checked this error is coming:

 

RAJATSH-M-V7QW:LIST_PYTHON rajatsh$ python3 RX_Rings.py

Please enter the file path: /Users/rajatsh/Downloads/ITTHK-TES-CLOUD-ASA-1

An error occurred: 'utf-8' codec can't decode byte 0xef in position 2116: invalid continuation byte

 

Easy way would be to rencode the input file as utf-8, refer to link below;

 

https://medium.com/code-kings/python3-fix-unicodedecodeerror-utf-8-codec-can-t-decode-byte-in-positi...

 

If you know a better solution, please comment and i will add it.

