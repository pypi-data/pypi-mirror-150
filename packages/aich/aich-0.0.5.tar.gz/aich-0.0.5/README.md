# AICH-Encryption
 Encryption Algorithm for All Languages. Generates a Token In Hindi. 

# Installation
sudo pip install aich

# Usage
from a2 import aich

search_word = input('Enter your encryption phrase:')

encrypted = aich.aichin(search_word)

print (encrypted)

search_word = input('Enter your decryption phrase:')

encrypted = aich.aichout(search_word)

print (encrypted)

# Encryption Example
{Inputs: This is freedom ये है आज़ादी , Outputs: षनफदपफदशफखकफयमफदशफखकफयमफददफखयफदषफदषफदनफदगफदतफयमफशयगफशनखफयमफशकशफशनपफयमफशमदफशणटफशकटफशकएफशयदफशनम}
{Inputs: AICH , Outputs: नणफनशफनकफनप}

# Decryption Example
{Inputs: षनफदपफदशफखकफयमफदशफखकफयमफददफखयफदषफदषफदनफदगफदतफयमफशयगफशनखफयमफशकशफशनपफयमफशमदफशणटफशकटफशकएफशयदफशनम, Outputs: This is freedom ये है आज़ादी}
{Inputs: नणफनशफनकफनप , Outputs: AICH}

