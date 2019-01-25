# from flask import current_app
# import unittest
# from api import app


# class TestDevelopmentConfig(unittest.TestCase):
    
#     def create_app(self):
#         app.config.from_object('config.DevelopmentConfig')
#         return app

#     def test_app_is_development(self):
#         with app.app_context():
#             self.assertTrue(app.config['DEBUG'] is True)
#             self.assertFalse(current_app is None)
#             self.assertTrue(
#                 app.config['DATABASE_URI'] == 'postgresql://irepo_dev:T3rr1613@localhost/db_ireporter_api' 
#             )

# class TestTestingConfig(unittest.TestCase):
    
#     def create_app(self):
#         with app.app_context():
#             app.config.from_object('config.TestingConfig')
#             return app

#     def test_app_is_testing(self):
        
#         self.assertTrue(app.config['DEBUG'])
#         self.assertTrue(
#                 app.config['DATABASE_URI'] == 'postgresql://irepo_dev:T3rr1613@localhost/pgtestdb'
#             )

# class TestProductionConfig(unittest.TestCase):
#     def create_app(self):
#         app.config.from_object('config.ProductionConfig')
#         return app

#     def test_app_is_production(self):
#         with app.app_context():
#             self.assertTrue(app.config['DEBUG'] is False)

