// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

/**
 * @title ANPRAuthorization
 * @dev A contract that manages vehicle plate authorization for an ANPR system,
 *      logs access events on the blockchain, and references IPFS for data storage.
 */
contract ANPRAuthorization {
    address public owner;

    /**
     * @dev Represents a vehicle in the system.
     * @param plate The license plate text (e.g., ABC123).
     * @param isAuthorized Whether this vehicle is currently authorized.
     */
    struct Vehicle {
        string plate;
        bool isAuthorized;
    }

    /**
     * @dev Stores vehicles by their plate number (converted to lowercase or a standard format).
     */
    mapping(bytes32 => Vehicle) private vehicles;

    /**
     * @dev Emitted when a vehicle is granted access.
     * @param plate The plate number recognized by the system.
     * @param gateOperator The address that called the authorization check (e.g., a gate controller).
     * @param timestamp The block timestamp for the event.
     * @param ipfsHash A reference to an IPFS record containing additional data (logs, images, etc.).
     */
    event AccessGranted(
        string indexed plate,
        address indexed gateOperator,
        uint256 timestamp,
        string ipfsHash
    );

    /**
     * @dev Emitted when a vehicle is denied access.
     * @param plate The plate number recognized by the system.
     * @param gateOperator The address that called the authorization check (e.g., a gate controller).
     * @param timestamp The block timestamp for the event.
     * @param ipfsHash A reference to an IPFS record containing additional data (logs, images, etc.).
     */
    event AccessDenied(
        string indexed plate,
        address indexed gateOperator,
        uint256 timestamp,
        string ipfsHash
    );

    /**
     * @dev Restricts function usage to the contract owner only.
     */
    modifier onlyOwner() {
        require(msg.sender == owner, "Not the contract owner");
        _;
    }

    /**
     * @dev Initializes the contract, setting the deployer as the owner.
     */
    constructor() {
        owner = msg.sender;
    }

    /**
     * @dev Registers a new vehicle or updates an existing one.
     * @param plate The vehicle's plate text.
     * @param authorized Whether the vehicle is authorized to enter.
     */
    function setVehicleAuthorization(string memory plate, bool authorized)
        external
        onlyOwner
    {
        bytes32 plateHash = _normalizePlate(plate);
        vehicles[plateHash] = Vehicle(plate, authorized);
    }

    /**
     * @dev Removes a vehicle from the authorization mapping.
     * @param plate The vehicle's plate text.
     */
    function removeVehicle(string memory plate) external onlyOwner {
        bytes32 plateHash = _normalizePlate(plate);
        delete vehicles[plateHash];
    }

    /**
     * @dev Checks if a vehicle is authorized, logs the access event,
     *      and references IPFS for storing additional data (e.g., images, logs).
     * @param plate The recognized plate text from OCR.
     * @param ipfsHash The IPFS hash referencing data for this event.
     * @return success A boolean indicating if the vehicle is authorized.
     */
    function checkAuthorization(string memory plate, string memory ipfsHash)
        external
        returns (bool success)
    {
        bytes32 plateHash = _normalizePlate(plate);
        Vehicle memory v = vehicles[plateHash];

        if (v.isAuthorized) {
            // Emit AccessGranted if the vehicle is authorized
            emit AccessGranted(plate, msg.sender, block.timestamp, ipfsHash);
            return true;
        } else {
            // Emit AccessDenied if the vehicle is not authorized
            emit AccessDenied(plate, msg.sender, block.timestamp, ipfsHash);
            return false;
        }
    }

    /**
     * @dev Returns the current authorization status of a plate.
     * @param plate The vehicle's plate text.
     */
    function getAuthorizationStatus(string memory plate) 
        external 
        view 
        returns (bool) 
    {
        bytes32 plateHash = _normalizePlate(plate);
        return vehicles[plateHash].isAuthorized;
    }

    /**
     * @dev Normalizes plate strings by converting them to lowercase
     *      to ensure consistent lookups.
     */
    function _normalizePlate(string memory plate)
        internal
        pure
        returns (bytes32)
    {
        // Convert to lower for case-insensitive matching
        // Then hash for easy mapping
        return keccak256(abi.encodePacked(_toLower(plate)));
    }

    /**
     * @dev Converts a string to lowercase (simple ASCII-only).
     */
    function _toLower(string memory str)
        internal
        pure
        returns (string memory)
    {
        bytes memory bStr = bytes(str);
        bytes memory bLower = new bytes(bStr.length);

        for (uint256 i = 0; i < bStr.length; i++) {
            // Uppercase char range
            if ((bStr[i] >= 0x41) && (bStr[i] <= 0x5A)) {
                // Convert to lowercase
                bLower[i] = bytes1(uint8(bStr[i]) + 32);
            } else {
                bLower[i] = bStr[i];
            }
        }
        return string(bLower);
    }
}

# dfx , cargo, rust