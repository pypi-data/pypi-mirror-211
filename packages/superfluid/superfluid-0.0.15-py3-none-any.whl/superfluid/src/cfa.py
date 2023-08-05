from typing import Optional

from web3 import Web3
from web3.types import TxParams
from web3.middleware import geth_poa_middleware
from web3.contract.contract import ContractFunction

from .host import Host
from .constants import CFA_V1_ABI, CFA_V1_FORWARDER_ABI
from .types import GetFlowParams, GetAccountFlowInfoParams, GetFlowOperatorDataParams, GetFlowOperatorDataParamsByID, CreateFlowParams, UpdateFlowParams, DeleteFlowParams, CreateFlowByOperatorParams, UpdateFlowByOperatorParams, Web3FlowInfo, UpdateFlowParams, Web3FlowOperatorData, FlowRateAllowanceParams, UpdateFlowOperatorPermissionsParams, FullControlParams
from .errors import SFError
from .operation import Operation
from .utils import get_network


class CFA_V1:

    def __init__(self, rpc: str, chain_id: int) -> None:
        self.rpc = rpc
        network = get_network(chain_id)
        web3 = Web3(Web3.HTTPProvider(rpc))
        web3.middleware_onion.inject(geth_poa_middleware, layer=0)
        self.host = Host(rpc, network.HOST)
        self.contract = web3.eth.contract(
            address=network.CFA_V1, abi=CFA_V1_ABI)
        self.forwarder = web3.eth.contract(
            address=network.CFA_V1_FORWARDER, abi=CFA_V1_FORWARDER_ABI)

    def get_flow(self, params: GetFlowParams) -> Web3FlowInfo:
        """
            Get the details of a flow.
            @param params - holds the super token, sender, and receiver
            @returns - Web3FlowInfo
        """
        try:
            transaction_response = self.contract.functions.getFlow(
                params.super_token, params.sender, params.receiver).call()
            info = {
                "timestamp": transaction_response[0],
                "flowRate": transaction_response[1],
                "deposit": transaction_response[2],
                "owedDeposit": transaction_response[3]
            }
            return info
        except Exception as e:
            raise SFError(
                "CFAV1_READ", "There was an error getting the flow", e)

    def get_account_flow_info(self, params: GetAccountFlowInfoParams) -> Web3FlowInfo:
        """
            Get the details of a account flow in a super token.
            @param params - holds the super token and account
            @returns - Web3FlowInfo
        """
        try:
            transaction_response = self.contract.functions.getAccountFlowInfo(
                params.super_token, params.account).call()
            info = {
                "timestamp": transaction_response[0],
                "flowRate": transaction_response[1],
                "deposit": transaction_response[2],
                "owedDeposit": transaction_response[3]
            }
            return info
        except Exception as e:
            raise SFError(
                "CFAV1_READ", "There was an error getting the account flow information", e)

    def get_net_flow(self, params: GetAccountFlowInfoParams) -> int:
        """
            Get the details of the net flow of an account in a super token.
            @param params - holds the super token and account
            @returns - int: net flow rate of the account
        """
        try:
            transaction_response = self.contract.functions.getNetFlow(
                params.super_token, params.account).call()
            net_flow_rate = transaction_response
            return net_flow_rate
        except Exception as e:
            raise SFError(
                "CFAV1_READ", "There was an error getting net flow", e)

    def get_flow_operator_data(self, params: GetFlowOperatorDataParams) -> Web3FlowOperatorData:
        """
            Get the details of a flow operator to a sender
            @param params - holds the super token, sender and flow operator
            @returns - Web3FlowOperatorData
        """
        try:
            transaction_response = self.contract.functions.getFlowOperatorData(
                params.super_token, params.sender, params.flow_operator).call()
            flow_operator_data = {
                # TODO: Review conversions
                "flowOperatorId": Web3.to_hex(transaction_response[0]),
                "permissions": transaction_response[1],
                "flowRateAllowance": transaction_response[2]
            }
            return flow_operator_data
        except Exception as e:
            raise SFError(
                "CFAV1_READ", "There was an error getting flow operator data", e)

    def get_flow_operator_data_by_id(self, params: GetFlowOperatorDataParamsByID) -> Web3FlowOperatorData:
        """
            Get the details of a flow operator to a sender by id
            @param params - holds the super token and the flow operator id
            @returns - Web3FlowOperatorData
        """
        try:
            transaction_response = self.contract.functions.getFlowOperatorDataByID(
                params.super_token, params.flow_operator_id).call()
            flow_operator_data = {
                # TODO: Review conversions
                "flowOperatorId": params.flow_operator_id,
                "permissions": transaction_response[0],
                "flowRateAllowance": transaction_response[1]
            }
            return flow_operator_data
        except Exception as e:
            raise SFError(
                "CFAV1_READ", "There was an error getting flow operator data", e)

    def create_flow(self, params: CreateFlowParams) -> Operation:
        """
            Creates a flow
            @param params - mainly holds the super token, sender, receiver and flow rate
            @returns - Operation
        """
        calldata = self.contract.encodeABI(fn_name='createFlow', args=[
            params.super_token, params.receiver, params.flow_rate, "0x"])
        call_agreement_operation = self.host.call_agreement(
            self.contract.address, calldata, params.user_data or "0x")
        forwarder_call: ContractFunction = self.forwarder.functions.createFlow(
            params.super_token, params.sender, params.receiver, params.flow_rate, params.user_data or "0x")
        return self._get_call_agreement_operation(call_agreement_operation, forwarder_call, params.should_use_call_agreement)

    def update_flow(self, params: UpdateFlowParams) -> Operation:
        """
            Updates a flow
            @param params - mainly holds the super token, sender, receiver and flow rate
            @returns - Operation
        """
        calldata = self.contract.encodeABI(fn_name='updateFlow', args=[
            params.super_token, params.receiver, params.flow_rate, "0x"])
        call_agreement_operation = self.host.call_agreement(
            self.contract.address, calldata, "0x")
        forwarder_call: ContractFunction = self.forwarder.functions.updateFlow(
            params.super_token, params.sender, params.receiver, params.flow_rate, params.user_data or "0x")
        return self._get_call_agreement_operation(call_agreement_operation, forwarder_call, params.should_use_call_agreement)

    def delete_flow(self, params: DeleteFlowParams) -> Operation:
        """
            Deletes a flow
            @param params - mainly holds the super token, sender, and receiver
            @returns - Operation
        """
        calldata = self.contract.encodeABI(fn_name='deleteFlow', args=[
            params.super_token, params.sender, params.receiver, "0x"])
        call_agreement_operation = self.host.call_agreement(
            self.contract.address, calldata, "0x")
        forwarder_call: ContractFunction = self.forwarder.functions.deleteFlow(
            params.super_token, params.sender, params.receiver, params.user_data or "0x")
        return self._get_call_agreement_operation(call_agreement_operation, forwarder_call, params.should_use_call_agreement)

    def increase_flow_rate_allowance(self, params: FlowRateAllowanceParams) -> Operation:
        """
            Increases the flow rate allowance of a flow operator
            @param params - holds the super token, flow operator, flow rate allowance delta and user data
            @returns - Operation
        """
        calldata = self.contract.encodeABI(fn_name='increaseFlowRateAllowance', args=[
            params.super_token, params.flow_operator, params.flow_rate_allowance_delta, "0x"])
        call_agreement_operation = self.host.call_agreement(
            self.contract.address, calldata, params.user_data or "0x")
        return call_agreement_operation

    def decrease_flow_rate_allowance(self, params: FlowRateAllowanceParams) -> Operation:
        """
            Decreases the flow rate allowance of a flow operator
            @param params - holds the super token, flow operator, flow rate allowance delta and user data
            @returns - Operation
        """
        calldata = self.contract.encodeABI(fn_name='decreaseFlowRateAllowance', args=[
            params.super_token, params.flow_operator, params.flow_rate_allowance_delta, "0x"])
        call_agreement_operation = self.host.call_agreement(
            self.contract.address, calldata, params.user_data or "0x")
        return call_agreement_operation

    def update_flow_operator_permissions(self, params: UpdateFlowOperatorPermissionsParams) -> Operation:
        """
            Update permissions for a flow operator as a sender.
            @param params - mainly holds the super token, flow operator, permissions, flow rate allowance and user data
            @returns - Operation
        """
        calldata = self.contract.encodeABI(fn_name='updateFlowOperatorPermissions', args=[
            params.super_token, params.flow_operator, params.permissions, params.flow_rate_allowance, "0x"])
        call_agreement_operation = self.host.call_agreement(
            self.contract.address, calldata, params.user_data or "0x")
        forwarder_call: ContractFunction = self.forwarder.functions.updateFlowOperatorPermissions(
            params.super_token, params.flow_operator, params.permissions, params.flow_rate_allowance)
        return self._get_call_agreement_operation(call_agreement_operation, forwarder_call, params.should_use_call_agreement)

    def authorize_flow_operator_with_full_control(self, params: FullControlParams) -> Operation:
        """
            Give flow operator full control - max flow rate and create/update/delete permissions.
            @param params - mainly holds the super token, flow operator, and user data
            @returns - Operation
        """
        calldata = self.contract.encodeABI(fn_name='authorizeFlowOperatorWithFullControl', args=[
            params.super_token, params.flow_operator, "0x"])
        call_agreement_operation = self.host.call_agreement(
            self.contract.address, calldata, params.user_data or "0x")
        forwarder_call: ContractFunction = self.forwarder.functions.grantPermissions(
            params.super_token, params.flow_operator)
        return self._get_call_agreement_operation(call_agreement_operation, forwarder_call, params.should_use_call_agreement)

    def revoke_flow_operator_with_full_control(self, params: FullControlParams) -> Operation:
        """
            Revoke flow operator control - set flow rate to 0 with no permissions.
            @param params - mainly holds the super token, flow operator, and user data
            @returns - Operation
        """
        calldata = self.contract.encodeABI(fn_name='revokeFlowOperatorWithFullControl', args=[
            params.super_token, params.flow_operator, "0x"])
        call_agreement_operation = self.host.call_agreement(
            self.contract.address, calldata, params.user_data or "0x")
        forwarder_call: ContractFunction = self.forwarder.functions.revokePermissions(
            params.super_token, params.flow_operator)
        return self._get_call_agreement_operation(call_agreement_operation, forwarder_call, params.should_use_call_agreement)

    def create_flow_by_operator(self, params: CreateFlowByOperatorParams) -> Operation:
        """
            Create a flow as an operator
            @param params - mainly holds the super token, sender, receiver and flow rate
            @returns - Operation
        """
        calldata = self.contract.encodeABI(fn_name='createFlowByOperator', args=[
            params.super_token, params.sender, params.receiver, params.flow_rate, "0x"])
        call_agreement_operation = self.host.call_agreement(
            self.contract.address, calldata, params.user_data or "0x")
        create_flow_operation = self.create_flow(params)
        return self._get_call_agreement_operation(call_agreement_operation, create_flow_operation.forwarder_call, params.should_use_call_agreement)

    def update_flow_by_operator(self, params: UpdateFlowByOperatorParams) -> Operation:
        """
            Update a flow as an operator
            @param params - mainly holds the super token, sender, receiver and flow rate
            @returns - Operation
        """
        calldata = self.contract.encodeABI(fn_name='updateFlowByOperator', args=[
            params.super_token, params.sender, params.receiver, params.flow_rate, "0x"])
        call_agreement_operation = self.host.call_agreement(
            self.contract.address, calldata, "0x")
        update_flow_operation = self.update_flow(params)
        return self._get_call_agreement_operation(call_agreement_operation, update_flow_operation.forwarder_call, params.should_use_call_agreement)

    def delete_flow_by_operator(self, params: DeleteFlowParams) -> Operation:
        """
            Delete a flow as an operator
            @param params - mainly holds the super token, sender, and receiver
            @returns - Operation
        """
        calldata = self.contract.encodeABI(fn_name='deleteFlowByOperator', args=[
            params.super_token, params.sender, params.receiver, "0x"])
        call_agreement_operation = self.host.call_agreement(
            self.contract.address, calldata, "0x")
        delete_flow_operation = self.delete_flow(params)
        return self._get_call_agreement_operation(call_agreement_operation, delete_flow_operation.forwarder_call, params.should_use_call_agreement)

    def _get_call_agreement_operation(self, call_agreement_operation: Operation, forwarder_call: Optional[ContractFunction] = None, should_use_call_agreement: Optional[bool] = None) -> Operation:
        if should_use_call_agreement == True:
            return call_agreement_operation
        else:
            return Operation(self.rpc, call_agreement_operation.agreement_call, call_agreement_operation.type, forwarder_call)
