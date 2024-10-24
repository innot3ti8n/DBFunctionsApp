import azure.functions as func
import logging
import mysql.connector
import os
from mysql.connector import errorcode
import json
from mysql.connector.errors import Error


dbConfig = {
    'host': os.environ['DB_HOST'],
    'database': os.environ['DB_DB'],
    'user': os.environ['DB_USR'],
    'password': os.environ['DB_PWD'],
    'ssl_ca': './DigiCertGlobalRootCA.pem',
    'ssl_disabled' : False
}

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

# GET: Get Criteria list for a skill
'''

    Route: '/criteria/{skillId:int?}'
    Route Params: {
        skillId: Int. Values are 1: Punctuation, 2: Vocabulary, 3: Cohesion, 4: Sentente Type & Structure, 5: Developing & Elaborating Ideas
    }
'''
@app.route(route="criteria/{skillId:int?}", methods=["GET"])
def criteria(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    id = req.route_params.get('skillId')

    try:
        conn = mysql.connector.connect(**dbConfig)
        logging.info("Connection Established")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with the username or password")
            return func.HttpResponse(body="Database Error", status_code=500)
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
            return func.HttpResponse(body="Database Error", status_code=500)
        else:
            print(err)
            print(**dbConfig)
            return func.HttpResponse(body=str(err), status_code=500)
    else:
        cursor = conn.cursor(dictionary=True)

    query = f"select C.criteria_id, S.skill_level_id, S.level_id, C.criteria from Criteria as C RIGHT join skill_level as S ON C.skill_level_id = S.skill_level_id WHERE skill_id = {id};"

    try:
        cursor.execute(query)
        result = cursor.fetchall()
        if result:
            return func.HttpResponse(json.dumps(result), status_code=200)
        else:
            return func.HttpResponse(None, status_code=204)
    finally:
        conn.close()

# GET: Get Text Component for a Specific Skill
'''
    Param: skillId (1: Punctuation, 2: Vocabulary, 3: Cohesion, 4: Sentente Type & Structure, 5: Developing & Elaborating Ideas)
    Route: text_component/{skillId:int?}
'''
@app.route(route="text_component/{skillId:int?}", methods=["GET"])
def textComponent(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    id = req.route_params.get('skillId')

    try:
        conn = mysql.connector.connect(**dbConfig)
        logging.info("Connection Established")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with the username or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
            print(**dbConfig)
    else:
        cursor = conn.cursor(dictionary=True)

    query = f"select * from text_component WHERE skill_id={id};"

    try:
        cursor.execute(query)
        result = cursor.fetchall()
        if result:
            return func.HttpResponse(json.dumps(result), status_code=200)
        else:
            return func.HttpResponse(None, status_code=204)
    finally:
        conn.close()

# POST: Send new Annotation Text Sample to DB 
# Request Body
'''
{
    "text": String,
    "annotationType": Number,
    "sampleId": Number,
}
'''
@app.route(route="text_sample_annotation", methods=["POST"])
def sendTextSampleAnnotation(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    body = req.get_json()

    try:
        body = req.get_json()
        textSampleContent = body["text"] if "text" in body.keys() else None
        annotatationType = body["annotationType"] if "annotationType" in body.keys() else None
        textSampleId = body["sampleId"] if "sampleId" in body.keys() and int(body["sampleId"]) != 0 else None
        skillLevelId = body["skillLevelId"] if "skillLevelId" in body.keys() else None

        if textSampleId == None or textSampleContent == None or annotatationType == None:
            return func.HttpResponse(body="Bad Request", status_code=400)
        
    except ValueError:
        print(f"Invalid Request body, {ValueError}")
        return func.HttpResponse(body=f"Invalid Request body, {ValueError}", status_code=400)

    try:
        conn = mysql.connector.connect(**dbConfig)
        logging.info("Connection Established")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with the username or password")
            return func.HttpResponse(body="Database Error", status_code=500)
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
            return func.HttpResponse(body="Database Error", status_code=500)
        else:
            print(err)
            print(**dbConfig)
            return func.HttpResponse(body=str(err), status_code=500)
    else:
        cursor = conn.cursor(dictionary=True)

    query = f"Insert into text_sample_annotation SET text_sample_id=%(textSampleId)s, annotation_type_id=%(annotatationType)s, text=%(text)s;"

    try:
        cursor.execute(query, {"textSampleId": textSampleId, "annotatationType": annotatationType, "text": textSampleContent})
        conn.commit()
        result = cursor.lastrowid
        
        if(skillLevelId):
            query = f"Insert into results SET text_sample_annotation_id={result}, skill_level_id={skillLevelId}"
            cursor.execute(query)
            conn.commit()

        return func.HttpResponse(json.dumps(result), status_code=200)
    finally:
        conn.close()

# GET: Get Annotation Text Sample
'''
route: '/text_sample_annotation/{text_sample_annotation_id:int?}'
Param: text_sample_annotation_id: Int
'''
@app.route(route="text_sample_annotation/{text_sample_annotation_id:int?}", methods=["GET"])
def getTextSampleAnnotation(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    id = req.route_params.get('text_sample_annotation_id')

    try:
        conn = mysql.connector.connect(**dbConfig)
        logging.info("Connection Established")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with the username or password")
            return func.HttpResponse(body="Something is wrong with the database", status_code=500)
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
            return func.HttpResponse(body="Database Error", status_code=500)
        else:
            print(err)
            print(**dbConfig)
            return func.HttpResponse(body=str(err), status_code=500)
    else:
        cursor = conn.cursor(dictionary=True)

    query = f"SELECT * from text_sample_annotation WHERE text_sample_annotation_id={id};"

    try:
        cursor.execute(query)
        result = cursor.fetchone()
        if result:
            return func.HttpResponse(json.dumps(result), status_code=200)
        else:
            return func.HttpResponse(None, status_code=204)
    finally:
        conn.close()


# POST: Text Sample Create New (student_name)
# Route: '/text_sample'
# Request Body
'''
{
    "student_name": String,
}
'''
@app.route(route="text_sample", methods=["POST"])
def sendTextSample(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        body = req.get_json()
        studentName = body["student_name"] if "student_name" in body.keys() else "John Scriibiseed"

        if studentName == None:
            return func.HttpResponse(body="Bad Request", status_code=400)
    except ValueError:
        print(f"Invalid Request body, {ValueError}")
        return func.HttpResponse(body=f"Invalid Request body, {ValueError}", status_code=400)

    try:
        conn = mysql.connector.connect(**dbConfig)
        logging.info("Connection Established")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with the username or password")
            return func.HttpResponse(body="Database Error", status_code=500)
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
            return func.HttpResponse(body="Database Error", status_code=500)
        else:
            print(err)
            print(**dbConfig)
            return func.HttpResponse(body=str(err), status_code=500)
    else:
        cursor = conn.cursor(dictionary=True)

    query = f"Insert into text_sample (text_sample_name) VALUES (%(student_name)s);"

    try:
        cursor.execute(query, {"student_name": studentName})
        conn.commit()
        result = cursor.lastrowid
        return func.HttpResponse(json.dumps(result), status_code=200)
    finally:
        conn.close()

@app.route(route="skills", methods=["GET"])
def getSkills(req: func.HttpRequest) -> func.HttpResponse:
    try:
        conn = mysql.connector.connect(**dbConfig)
        logging.info("Connection Established")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with the username or password")
            return func.HttpResponse(body="Database Error", status_code=500)
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
            return func.HttpResponse(body="Database Error", status_code=500)
        else:
            print(err)
            print(**dbConfig)
            return func.HttpResponse(body=str(err), status_code=500)
    else:
        cursor = conn.cursor(dictionary=True)

    query = f"SELECT * FROM `skill`;"

    try:
        cursor.execute(query)
        result = cursor.fetchall()
        if result:
            return func.HttpResponse(json.dumps(result), status_code=200)
        else:
            return func.HttpResponse(None, status_code=204)
    finally:
        conn.close()

@app.route(route="flags", methods=["GET"])
def getFlags(req: func.HttpRequest) -> func.HttpResponse:
    try:
        conn = mysql.connector.connect(**dbConfig)
        logging.info("Connection Established")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with the username or password")
            return func.HttpResponse(body="Database Error", status_code=500)
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
            return func.HttpResponse(body="Database Error", status_code=500)
        else:
            print(err)
            print(**dbConfig)
            return func.HttpResponse(body=str(err), status_code=500)
    else:
        cursor = conn.cursor(dictionary=True)

    query = f"select * from `flag`;"

    try:
        cursor.execute(query)
        result = cursor.fetchall()
        if result:
            return func.HttpResponse(json.dumps(result), status_code=200)
        else:
            return func.HttpResponse(None, status_code=204)
    except mysql.connector.Error as e:
        print("Something went wrong: {}".format(err))
        return None
    finally:
        conn.close()

@app.route(route="flags/{skillId:int?}", methods=["GET"])
def getFlagsForTextComponents(req: func.HttpRequest) -> func.HttpResponse:

    skillId = req.route_params.get('skillId')

    try:
        conn = mysql.connector.connect(**dbConfig)
        logging.info("Connection Established")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with the username or password")
            return func.HttpResponse(body="Database Error", status_code=500)
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
            return func.HttpResponse(body="Database Error", status_code=500)
        else:
            print(err)
            print(**dbConfig)
            return func.HttpResponse(body=str(err), status_code=500)
    else:
        cursor = conn.cursor(dictionary=True)

    query = f"select c.text_component_id, cf.flag_id, c.markup_id from text_component as c INNER JOIN text_component_flag as cf ON c.text_component_id = cf.text_component_id WHERE skill_id=%(skillId)s;"

    try:
        cursor.execute(query, {"skillId": skillId})
        flags = cursor.fetchall()
        if flags:
            cursor.close()
        else:
            return func.HttpResponse(json.dumps({"msg": "Flags database error"}), status_code=500)
    except mysql.connector.Error as e:
        print("Something went wrong: {}".format(err))
        return None
    else:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(f"select * from text_component WHERE skill_id={skillId};")
            textComponents = cursor.fetchall()

            if textComponents:
                flagArray = []
                
                for textComponent in textComponents:
                    for flag in flags:
                        if int(flag["text_component_id"]) == int(textComponent["text_component_id"]):
                            flagArray.append(flags) # flag is being add twice
                    
                    textComponent["flags"] = flagArray

                return func.HttpResponse(json.dumps({"flags": flags, "textComponent": textComponents}), status_code=200)
            else:
                return func.HttpResponse(None, status_code=204)

        except mysql.connector.Error as e:
            print("Something went wrong: {}".format(err))
            return None