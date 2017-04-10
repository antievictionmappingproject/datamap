core.config = {
    "mobile": {
        "scale": false
    }, 
    "header": {
        "logo": "Your Logo", 
        "right": []
    }, 
    "ctmap": {
        "city": "san francisco", 
        "center": {
            "lat": 37.75, 
            "lng": -122.45
        }, 
        "geokeys": [
            "AIzaSyCgnoy4AYjX5qblebjf8HASGyHhnCZYMkQ",
            "AIzaSyDW-yuqN1MeX06PDburFj76rf6LhUoSuOc"
        ],
        "custom_kinds": ["eviction", "fire", "lord", "murder"],
        "types": ["building", "owner", "eviction", "fire"], 
        "queries": [
            {
                modelName: "owner",
                order: "-building.owner"
            }, {
                modelName: "building",
                order: "-parcel.building"
            }, {
                modelName: "building",
                order: "-eviction.building"
            }, {
                modelName: "fire",
                order: "-persons"
            }, {
                modelName: "policemurder"
            }
        ],
        "live": {
            "scouts": ["default"],
            "obstacles": ["default"],
            "objectives": ["default", "red"]
        }
    }, 
    "log": {
        "exclude": [], 
        "include": []
    }, 
    "css": []
};