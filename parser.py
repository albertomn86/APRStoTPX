import aprslib
from datetime import datetime, timezone
import re

packets = [
    '2024-10-19 18:10:19 +0200: EA7KOO-7>APLRT1,WIDE1-1,QB0M6,qAS,EA7KOO-10:!/;d`jM[+a[RYQ',
    '2024-10-19 18:11:23 +0200: EA7KOO-7>APLRT1,WIDE1-1,Q00L2,qAS,EA7KOO-10:!/;dbJM[,l[RZQ',
    '2024-10-19 18:13:26 +0200: EA7KOO-7>APLRT1,WIDE1-1,Q01L0,qAS,EA7KOO-10:!/;deWM[..[R]Q',
    '2024-10-19 18:14:45 +0200: EA7KOO-7>APLRT1,WIDE1-1,Q00K8,qAS,EA7KOO-10:!/;dg{M[.r[R`Q',
]

def main():
    for packet in packets:
        block = packet.split(' ')[3]
        date = re.search(r"(^.*\+0200)", packet)[0]

        format_str = '%Y-%m-%d %H:%M:%S %z'
        datetime_obj = datetime.strptime(date, format_str)

        utcdate = datetime.fromtimestamp(datetime_obj.timestamp(), tz=timezone.utc)

        formated_date = utcdate.isoformat().split('+')[0] + 'Z'
        try:
            decoded_packet = aprslib.parse(block)

            print(f"""
					<Trackpoint>
						<Time>{formated_date}</Time>
						<Position>
							<LatitudeDegrees>{round(decoded_packet.get("latitude"), 8)}</LatitudeDegrees>
							<LongitudeDegrees>{round(decoded_packet.get("longitude"), 8)}</LongitudeDegrees>
						</Position>
					</Trackpoint>"""
            )
        except:
            print("")


if __name__ == "__main__":
    main()