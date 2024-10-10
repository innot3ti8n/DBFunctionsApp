import unittest
import azure.functions as func
import json
import os

from function_app import sendTextSample, sendTextSampleAnnotation, getSkills, getTextSampleAnnotation, criteria, textComponent

class TestFunction(unittest.TestCase):

    def test_checkValidTextSample(self):
        req = func.HttpRequest(method='GET', url='/text_sample_annotation', route_params={'text_sample_annotation_id': 12}, body={None})

        func_call = getTextSampleAnnotation.build().get_user_function()
        resp = func_call(req)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(json.loads(resp.get_body()), {
            "text_sample_annotation_id": 12,
            "text_sample_id": 3,
            "annotation_type_id": 1,
            "text": "I love to eat Pho, Banh Mi and Bun Bo Hue"
        })

    def test_checkInValidTextSample(self):
        req = func.HttpRequest(method='GET', url='/text_sample_annotation', route_params={'text_sample_annotation_id': 0}, body={None})

        func_call = getTextSampleAnnotation.build().get_user_function()
        resp = func_call(req)

        self.assertEqual(resp.status_code, 204)
        self.assertEqual(resp.get_body(), b'')

    def test_validskillLists(self):
        req = func.HttpRequest(method='GET', url='/skills/', body={None})

        func_call = getSkills.build().get_user_function()
        resp = func_call(req)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(json.loads(resp.get_body()), [
            {
                "skill_id": 1,
                "name": "Punctuation",
                "text_component_count": 14
            },
            {
                "skill_id": 2,
                "name": "Vocabulary",
                "text_component_count": 14
            },
            {
                "skill_id": 3,
                "name": "Cohesion",
                "text_component_count": 13
            },
            {
                "skill_id": 4,
                "name": "Sentence Type and Structure",
                "text_component_count": 9
            },
            {
                "skill_id": 5,
                "name": "Developing and Elaborating Ideas",
                "text_component_count": 10
            }
        ])

    def test_ValidCriteriaList(self):
        req = func.HttpRequest(method='GET', url='/criteria', route_params={'skillId': 1}, body={None})

        expectedResponse = [{"criteria_id": 0, "skill_level_id": 1, "level_id": 1, "criteria": "This is the placeholder critera for level 0 for Punctuation"}, {"criteria_id": None, "skill_level_id": 2, "level_id": 2, "criteria": None}, {"criteria_id": 1, "skill_level_id": 3, "level_id": 3, "criteria": "This is the placeholder critera for level 1 for Punctuation"}, {"criteria_id": None, "skill_level_id": 4, "level_id": 4, "criteria": None}, {"criteria_id": 2, "skill_level_id": 5, "level_id": 5, "criteria": "This is the placeholder critera for level 2 for Punctuation"}, {"criteria_id": None, "skill_level_id": 6, "level_id": 6, "criteria": None}, {"criteria_id": 3, "skill_level_id": 7, "level_id": 7, "criteria": "This is the placeholder critera for level 3 for Punctuation"}, {"criteria_id": None, "skill_level_id": 8, "level_id": 8, "criteria": None}, {"criteria_id": 4, "skill_level_id": 9, "level_id": 9, "criteria": "Sentence boundary punctuation is correct (? . !) (occasional error is okay)\nCapitalises proper nouns & key events (Easter).\nCommas used for lists and \u2018some\u2019 other uses (eg, quotes, dates, adding pauses).\nMostly correct use of possessive apostrophes.\nUses quotes for simple dialogue.\n\nDefinitions:\nSingular Possessive: Tim\u2019s ball.\nPlural Possessive: Children\u2019s toys."}, {"criteria_id": None, "skill_level_id": 10, "level_id": 10, "criteria": None}, {"criteria_id": 5, "skill_level_id": 11, "level_id": 11, "criteria": "Can accurately use a range of simple  ? \u2018 , !  \u201d \u201c punctuation to support meaning.\n\u2018Mostly\u2019 correct comma usage to separate clauses.\nAccurate markers enable smooth reading.\n\nDefinitions:\nClauses separated by a comma: As I spoke, my heart raced."}, {"criteria_id": None, "skill_level_id": 12, "level_id": 12, "criteria": None}, {"criteria_id": 6, "skill_level_id": 13, "level_id": 13, "criteria": "Accurately uses simple ? \u2018 , !  \u201d \u201c punctuation.\nExperimenting with complex ; : \u2013 ... ( ) punctuation.\nCorrect comma usage to separate clauses, including subordinating clauses.\nPunctuates more complex dialogue correctly.\n\nDefinitions:\nComplex dialogue: \u201cI don\u2019t want to leave,\u201d she said, hesitating. \u201cBut I think it will be best\u201d."}, {"criteria_id": None, "skill_level_id": 14, "level_id": 14, "criteria": None}, {"criteria_id": 7, "skill_level_id": 15, "level_id": 15, "criteria": "This is the placeholder critera for level 7 for Punctuation"}, {"criteria_id": None, "skill_level_id": 16, "level_id": 16, "criteria": None}, {"criteria_id": 8, "skill_level_id": 17, "level_id": 17, "criteria": "This is the placeholder critera for level 8 for Punctuation"}, {"criteria_id": None, "skill_level_id": 18, "level_id": 18, "criteria": None}, {"criteria_id": 9, "skill_level_id": 19, "level_id": 19, "criteria": "This is the placeholder critera for level 9 for Punctuation"}, {"criteria_id": None, "skill_level_id": 20, "level_id": 20, "criteria": None}, {"criteria_id": 10, "skill_level_id": 21, "level_id": 21, "criteria": "This is the placeholder critera for level 10 for Punctuation"}]

        func_call = criteria.build().get_user_function()
        resp = func_call(req)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(json.loads(resp.get_body()), expectedResponse)
    
    def test_invalidCriteriaList(self):
        req = func.HttpRequest(method='GET', url='/criteria', route_params={'skillId': 6}, body={None})

        func_call = criteria.build().get_user_function()
        resp = func_call(req)
        
        self.assertEqual(resp.status_code, 204)

    def test_validTextComponent(self):
        req = func.HttpRequest(method='GET', url='text_component', route_params={'skillId': 2}, body={None})

        func_call = textComponent.build().get_user_function()

        expectedResponse = [{"text_component_id": 15, "skill_id": 2, "name": "word - expressive adjective", "example": "This ia a placeholder example for Word - Expressive Adjective", "markup_id": 1}, {"text_component_id": 16, "skill_id": 2, "name": "word - express feelings", "example": "This ia a placeholder example for Word - Express Feelings", "markup_id": 1}, {"text_component_id": 17, "skill_id": 2, "name": "word - opinion", "example": "This ia a placeholder example for Word - Opinion", "markup_id": 1}, {"text_component_id": 18, "skill_id": 2, "name": "word - expressive verbs", "example": "This ia a placeholder example for Word - Expressive Verbs", "markup_id": 1}, {"text_component_id": 19, "skill_id": 2, "name": "word - expressive adverbs", "example": "This ia a placeholder example for Word - Expressive Adverbs", "markup_id": 1}, {"text_component_id": 20, "skill_id": 2, "name": "word - learnt topic", "example": "This ia a placeholder example for Word - Learnt Topic", "markup_id": 1}, {"text_component_id": 21, "skill_id": 2, "name": "word - technical", "example": "This ia a placeholder example for Word - Technical", "markup_id": 1}, {"text_component_id": 22, "skill_id": 2, "name": "word - alternate", "example": "This ia a placeholder example for Word - Alternate", "markup_id": 1}, {"text_component_id": 23, "skill_id": 2, "name": "word - precise", "example": "This ia a placeholder example for Word - Precise", "markup_id": 1}, {"text_component_id": 24, "skill_id": 2, "name": "word - groups", "example": "This ia a placeholder example for Word - Groups", "markup_id": 1}, {"text_component_id": 25, "skill_id": 2, "name": "word - homonym", "example": "This ia a placeholder example for Word - Homonym", "markup_id": 1}, {"text_component_id": 26, "skill_id": 2, "name": "discipline-specific term", "example": "This ia a placeholder example for Discipline-Specific Term", "markup_id": 1}, {"text_component_id": 27, "skill_id": 2, "name": "evaluative language", "example": "This ia a placeholder example for Evaluative Language", "markup_id": 1}, {"text_component_id": 28, "skill_id": 2, "name": "shades of meaning", "example": "This ia a placeholder example for Shades of Meaning", "markup_id": 1}]

        resp = func_call(req)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(json.loads(resp.get_body()), expectedResponse)

    def test_invalidTextComponent(self):
        req = func.HttpRequest(method='GET', url='/text_component', route_params={'skillId': 6}, body={None})

        func_call = textComponent.build().get_user_function()
        resp = func_call(req)
        
        self.assertEqual(resp.status_code, 204)

    def test_SendSampleInfo(self):

        reqBody = json.dumps({"student_name": "Minh"}).encode()

        req = func.HttpRequest(method='POST',
                               url='/text_sample',
                               body=reqBody)

        func_call = sendTextSample.build().get_user_function()
        resp = func_call(req)

        self.assertEqual(resp.status_code, 200)
        self.assertTrue(str(resp.get_body().decode("utf-8")).isdigit())

    def test_sendTextSampleAnnotation(self):
        reqBody = json.dumps({"annotationType": 1,"sampleId": 4,"text": "I love Vietnamese food"}).encode()

        req = func.HttpRequest(method='POST',
                               url='/text_sample',
                               body=reqBody)

        func_call = sendTextSampleAnnotation.build().get_user_function()
        resp = func_call(req)

        self.assertEqual(resp.status_code, 200)
        self.assertTrue(str(resp.get_body().decode("utf-8")).isdigit())
