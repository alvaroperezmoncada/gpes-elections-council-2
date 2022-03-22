from simple_salesforce import Salesforce

params = [
    'Name', 'Income_ultimos_12_meses_CONSEJO__c', 'DNI__c', 'Birthdate', 'AlizeConstituentID__c', 'MailingPostalCode',
    'Email', 'Fecha_de_antiguedad__c', 'Activation_Date__c', 's360a__ContactCodes__c', 's360a__ContactType__c'
]


class MultipleContactsError(RuntimeError):
    pass


def salesforce_object():
    return Salesforce(

    )


def check_dni_and_zip_code(dni, zip_code):
    info = get_contact_by_dni_zip(dni, zip_code)
    return info


def check_dni_salesforce(dni):
    info = get_contact(dni, dni)
    return info


def searchContacts(search_string):
    sf = salesforce_object()
    response = sf.search('''find {{{}}} 
        in name fields 
        returning contact({} 
            where s360a__ContactCodes__c = 'Active Donor')
        limit 100    
        '''.format(search_string, params))
    return response['searchRecords']


def get_contact(email, dni_number, return_list=False):
    limit = 100 if return_list else 1
    ret = []
    sf_conn = salesforce_object()

    response = sf_conn.query(
        f"""
       SELECT {','.join(params)}
       FROM Contact
       WHERE DNI__c = '{dni_number}' AND s360a__ContactCodes__c = 'Active Donor'
       LIMIT {limit}
       """
    )
    objects = response['records']
    if len(objects) == 1 and not return_list:
        return objects[0]
    else:
        ret += objects

    if ret and not return_list:
        raise MultipleContactsError()
    return ret


def get_contact_by_dni_zip(dni_number, zip_code):
    limit = 1
    ret = []
    sf_conn = salesforce_object()

    response = sf_conn.query(
        f"""
       SELECT {','.join(params)}
       FROM Contact
       WHERE DNI__c = '{dni_number}' AND s360a__ContactCodes__c = 'Active Donor' AND MailingPostalCode = '{zip_code}'
       LIMIT {limit}
       """
    )
    objects = response['records']
    if len(objects) == 1:
        return objects[0]

    return ret
