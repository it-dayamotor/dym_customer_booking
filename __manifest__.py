{
    "name":"DYM CUSTOMER BOOKING",
    "version":"1.0",
    "author":"ALDRIAN",
    "category":"Custom Module",
    "description": """
        Customer Booking
    """,
    "depends":[
        "base",
        "mail",
        "website",
        "dym_website",
    ],
    "data":[   
        "security/ir.model.access.csv","views/assets.xml",
        "views/dym_customer_booking_web_view.xml",
        "views/dym_booking_service_view.xml",
        # data
        'data/schedule_action.xml',
        
    ],
    "active":False,
    "installable":True,
}