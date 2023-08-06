from flask import request
from flask_restx import Resource, fields
from ...db.db_connection import database_access
from ...namespace import api
import logging
from ...response_helper import get_response
import json
from bson import json_util


post_vehicle_details = api.model("vehicle_details", {
	"vehicle_no": fields.String,
	"plant_code": fields.String,
	"transporter_name": fields.String,
	"transporter_code": fields.String,
	"capacity": fields.String,
	"empty_weight": fields.String,
	"vehicle_type": fields.String,
	"engine_number": fields.String,
	"chasis_number": fields.String,
	"puc_number": fields.String,
	"puc_issue_date": fields.String,
	"puc_expiry_date": fields.String,
	"fitness_issue": fields.String,
	"fitness_expiry": fields.String,
	"insurance_number": fields.String,
	"insurance_issue_date": fields.String,
	"insurance_expiry_date": fields.String,
	"vehicle_owner_name": fields.String,
})


class TruckMaster(Resource):
	def get(self):
		try:
			database_connection = database_access()
			truck_details_col = database_connection["truck_master"]
			data = truck_details_col.find()
			if len(list(data)):
				data = truck_details_col.find()
				_response = get_response(200)
				_response["data"] = json.loads(json_util.dumps(data))
				return _response
			else:
				return get_response(404)
		except Exception as e:
			_response = get_response(404)
			_response['message'] = 'Failed to Get Truck Detail'
			logging.error(e)
			return _response

	@api.expect(post_vehicle_details)
	def post(self):
		args = request.get_json()
		try:
			database_connection = database_access()
			truck_details_col = database_connection["truck_master"]
			if not truck_details_col.find_one({"vehicle_no": args["vehicle_no"]}):
				truck_details_col.insert_one({
					"vehicle_no": args["vehicle_no"], "plant_code": args["plant_code"], "transporter_name": args["transporter_name"],
					"transporter_code": args["transporter_code"], "capacity": args["capacity"], "empty_weight": args["empty_weight"],
					"vehicle_type": args["vehicle_type"], "engine_number": args["engine_number"], "puc_number": args["puc_number"],
					"puc_issue_date": args["puc_issue_date"], "puc_expiry_date": args["puc_expiry_date"],
					"fitness_issue": args["fitness_issue"], "fitness_expiry": args["fitness_expiry"],
					"insurance_number": args["insurance_number"], "insurance_issue_date": args["insurance_issue_date"],
					"insurance_expiry_date": args["insurance_expiry_date"], "vehicle_owner_name": args["vehicle_owner_name"],
				})
				logging.info(get_response(200))
				return get_response(200)
			else:
				logging.info(get_response(409))
				return get_response(409)
		except Exception as e:
			_response = get_response(404)
			_response['message'] = 'Failed to Store Truck Details'
			logging.error(e)
			return _response


post_outbound_integration = api.model("outbound_details", {
	"trip_id": fields.String,
	"vehicle_number": fields.String,
	"movement_type": fields.String,
	"stage": fields.String,
	"check_status": fields.String,
	"check_time": fields.String,
})


class OutboundIntegration(Resource):
	def get(self):
		try:
			database_connection = database_access()
			outbound_integration_col = database_connection["outbound_integration"]
			data = outbound_integration_col.find()
			if len(list(data)):
				data = outbound_integration_col.find()
				_response = get_response(200)
				_response["data"] = json.loads(json_util.dumps(data))
				return _response
			else:
				return get_response(404)
		except Exception as e:
			_response = get_response(404)
			_response['message'] = 'Failed to Get Outbound Integration Detail'
			logging.error(e)
			return _response

	@api.expect(post_outbound_integration)
	def post(self):
		args = request.get_json()
		try:
			database_connection = database_access()
			outbound_integration_col = database_connection["outbound_integration"]
			if not outbound_integration_col.find_one({"vehicle_number": args["vehicle_number"]}):
				outbound_integration_col.insert_one({
					"trip_id": args["trip_id"], "vehicle_number": args["vehicle_number"],
					"movement_type": args["movement_type"], "stage": args["stage"], "check_status": args["check_status"],
					"check_time": args["check_time"],
					})
				logging.info(get_response(200))
				return get_response(200)
			else:
				logging.info(get_response(409))
				return get_response(409)
		except Exception as e:
			_response = get_response(404)
			_response['message'] = 'Failed to Store Outbound Details'
			logging.error(e)
			return _response


post_integration_trigger = api.model("integration_trigger", {
	"trip_id": fields.String,
	"vehicle_number": fields.String,
	"movement_type": fields.String,
})


class IntegrationTrigger(Resource):
	def get(self):
		try:
			database_connection = database_access()
			integration_trigger_col = database_connection["integration_trigger"]
			data = integration_trigger_col.find()
			if len(list(data)):
				data = integration_trigger_col.find()
				_response = get_response(200)
				_response["data"] = json.loads(json_util.dumps(data))
				return _response
			else:
				return get_response(404)
		except Exception as e:
			_response = get_response(404)
			_response['message'] = 'Failed to Get Integration Trigger Detail'
			logging.error(e)
			return _response

	@api.expect(post_integration_trigger)
	def post(self):
		args = request.get_json()
		try:
			database_connection = database_access()
			integration_trigger_col = database_connection["integration_trigger"]
			if not integration_trigger_col.find_one({"vehicle_number": args["vehicle_number"]}):
				integration_trigger_col.insert_one(
					{
						"trip_id": args["trip_id"], "vehicle_number": args["vehicle_number"], "movement_type": args["movement_type"]
					})
				logging.info(get_response(200))
				return get_response(200)
			else:
				logging.info(get_response(409))
				return get_response(409)
		except Exception as e:
			_response = get_response(404)
			_response['message'] = 'Failed to Store Integration Trigger Details'
			logging.error(e)
			return _response


post_stage_master = api.model("StageMaster", {
	"stages": fields.Raw(
		[],
		required=True,
		example=[

		]
	)
})


class StageMaster(Resource):
	def get(self):
		try:
			database_connection = database_access()
			stage_master_col = database_connection["stage_master"]
			data = stage_master_col.find()
			if len(list(data)):
				data = stage_master_col.find()
				_response = get_response(200)
				_response["data"] = json.loads(json_util.dumps(data))
				return _response
			else:
				return get_response(404)
		except Exception as e:
			_response = get_response(404)
			_response['message'] = 'Failed to Get Stage Master Detail'
			logging.error(e)
			return _response

	@api.expect(post_stage_master)
	def post(self):
		args = request.get_json()
		try:
			print(args)
			database_connection = database_access()
			stage_master_col = database_connection["stage_master"]
			stage_master_col.insert_one(
				{
					"stages": args["stages"]
				})
			logging.info(get_response(200))
			return get_response(200)
		except Exception as e:
			_response = get_response(404)
			_response['message'] = 'Failed to Store Stages Details'
			logging.error(e)
			return _response
