# models.py
class Shipment:
    def __init__(self, date_of_shipment, date_of_delivery, vehicle_type, vehicle_no, employee, client):
        self.date_of_shipment = date_of_shipment
        self.date_of_delivery = date_of_delivery
        self.vehicle_type = vehicle_type
        self.vehicle_no = vehicle_no
        self.employee = employee
        self.client = client

        def to_dict(self):
            return {
                'date_of_shipment': self.date_of_shipment,
                'date_of_delivery': self.date_of_delivery,
                'vehicle_type': self.vehicle_type,
                'vehicle_no': self.vehicle_no,
                'employee': self.employee,
                'client': self.client
            }