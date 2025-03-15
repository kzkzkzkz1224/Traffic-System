# traffic_controller.py
def control_traffic_lights(predicted_congestion, road):
    """
    Suggests traffic light actions based on predicted congestion for a specific road.
    """
    if predicted_congestion > 0.8:
        return f"Extend green time on {road}"
    elif predicted_congestion > 0.5:
        return f"Normal operation on {road}"
    else:
        return f"Reduce green time on {road}"

# Test the function
if __name__ == "__main__":
    congestion_level = 0.9
    road = "Route 10"
    action = control_traffic_lights(congestion_level, road)
    print(f"Predicted Congestion: {congestion_level}, Action: {action}")