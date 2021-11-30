from simple_salesforce import Salesforce

params = [
    'Name', 'Income_ultimos_12_meses_CONSEJO__c', 'DNI__c', 'Birthdate', 'AlizeConstituentID__c', 'MailingPostalCode',
    'Email', 'Fecha_de_antiguedad__c', 'Activation_Date__c', 's360a__ContactCodes__c', 's360a__ContactType__c'
]


class MultipleContactsError(RuntimeError):
    pass


def get_contact(email, dni_number, return_list=False):
    limit = 100 if return_list else 2
    ret = []
    sf_conn = Salesforce(

    )
    response = sf_conn.query(
        f"""
       SELECT {','.join(params)}
       FROM Contact
       WHERE Email = '{email}' AND s360a__ContactCodes__c = 'Donor Prospect'
       LIMIT {limit}
       """
    )
    objects = response['records']
    if len(objects) == 1 and not return_list:
        return objects[0]
    else:
        ret += objects

    response = sf_conn.query(
        f"""
       SELECT {','.join(params)}
       FROM Contact
       WHERE DNI__c = '{dni_number}' AND s360a__ContactCodes__c = 'Donor Prospect'
       LIMIT {limit}
       """
    )
    objects = response['records']
    if len(objects) == 1 and not return_list:
        return objects[0]
    else:
        ret += objects

    response = sf_conn.query(
        f"""
           SELECT {','.join(params)}
           FROM Contact
           WHERE DNI__c = '{dni_number}' AND s360a__ContactCodes__c = 'Donor Prospect' AND Email = '{email}'
           LIMIT {limit}
           """
    )
    objects = response['records']
    if len(objects) == 1:
        return objects[0]
    else:
        ret += objects

    if ret and not return_list:
        raise MultipleContactsError()
    return ret
