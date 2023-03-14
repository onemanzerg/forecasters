async def check_valid_score(forecast):

    if ":" not in forecast:
        return False
    else:
        goal_list = [point.strip() for point in forecast.split(":")]
        check = all(map(lambda x: x.isdigit(), goal_list))
    return check


