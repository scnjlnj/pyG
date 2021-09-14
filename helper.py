import json

def geo_polygon_to_listpoint(data:dict):
    points = []
    for area in data["coordinates"]:
        for point in area:
            points.append({"type":"Point", "coordinates":point})
        #只返回第一个区域
        break
    return points

if __name__ == '__main__':
    data = """{"type":"Polygon","coordinates":[[[118.7974,26.5644],[118.8006,26.5640],[118.8004,26.5638],[118.7975,26.5641],[118.7974,26.5644]]]}"""
    json_dict = json.loads(data)
    ret_str = json.dumps(geo_polygon_to_listpoint(json_dict))
    print(ret_str)