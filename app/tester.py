import dbaser, helper
from datetime import datetime, timedelta
from sqlalchemy import select
from dbaser import Consultation

session = helper.getSession()

dc = 0
target_date = datetime.now() - timedelta(days=2)
stt = select(Consultation).where(Consultation.date_limite_depot > target_date)
consultations = session.scalars(stt).all()
for c in consultations:
    print(f'=============================== {c.portal_id}')
    dbaser.deleteCons(c.portal_id, session)
    dc += 1

print(f'=====================##############-{dc}-########')



# try: cleaner.removeOldDce(session)
# except Exception as x : print(str(x))
# finally :
#     if session:
#         print('Closing session.')
#         session.close()
