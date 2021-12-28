import datetime
from datetime import timezone

year         = 2021 
month        = 1
day          = 5
hours        = 00 
minutes      = 00
seconds      = 00
milliseconds = 00

dt = datetime.datetime( year, month, day, hours, minutes, seconds,  milliseconds ) 
print( '\n\n date time: {}'.format( dt ) )

utc_time = dt.replace(tzinfo=timezone.utc)
utc_timestamp = utc_time.timestamp()
print( 'utc: {} \n'.format( utc_timestamp )  )


