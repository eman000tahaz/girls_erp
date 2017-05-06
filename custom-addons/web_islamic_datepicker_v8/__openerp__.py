{
    "name": "Islamic Datepicker",
    'version': '1.0',
    'author': 'Techorg',
    'summary': 'Web tool',
    "description":
        """
        OpenERP Web Display Islamic Datepicker.
        =======================================================
The Islamic calendar (or Hijri calendar) is a purely lunar calendar. It contains 12 months that are based on the motion of the moon, and because 12 synodic months is only 12 x 29.53=354.36 days, the Islamic calendar is consistently shorter than a tropical year.

The calendar is based on the Qur'an (Sura IX, 36-37) and its proper observance is a sacred duty for Muslims.

The Islamic calendar is the official calendar in countries around the Gulf, especially Saudi Arabia. But other Muslim countries use the Gregorian calendar for civil purposes and only turn to the Islamic calendar for religious purposes.

        
        """,
    'website': 'www.techorg.com',
    "depends": ['web'],
    'category': 'web',
    'sequence': 17,
    'data': [
         "res_users_view.xml",
         "views/web_linkedin.xml"    
    ],
   
    'qweb' : [
        "static/src/xml/*.xml",
    ],
        'images': ['images/1.jpg','images/2.jpg'],
    'installable': True,    
    'auto_install': False,
}
