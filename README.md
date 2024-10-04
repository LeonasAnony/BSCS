# Bürger Service Center Script
A script to automaticlly fetch appiontments at the BSC's in Bremen, Germany from their Website and alert you if it is before a speciffied date.
This script does NOT book the appiontment.

## How-To
1.  Install required packages: ```pip install -r requirements.txt```
2. Change the options in ```main.py```
	1.  ```soll_vor_datum```  sets the date till which the appiontment should be.
	2. ```location_url``` sets the BSC to search the appointment at. Normaly only ```md=?``` needs to be changed.
	3. ```date_url``` sets the typ of appointment to be fetched. ```mdt=?``` and ```cnc-????=1``` need to be changed.
	4. ```webhook_url``` sets the url of a webhook to be called when an appiontment is found. Optional.
	5. ```sound``` sets whether a sound should be played when an appiontmenr is found.
	6. ```interval``` sets the interval at which the Website should be fetched. Min: 10. Default: 60.
	7. ```server``` sets whether the script is run on a server.
3. Run the script: ```python main.py```
4. If the fetched date is before the set date, the fetched date will be printed in green. Accorting to the configured options a sound will be played and the webhook will be called. The script will exit.
