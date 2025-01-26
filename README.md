# Energy Identification

This custom component identifies appliances based on their energy usage patterns using a machine learning model.

## Installation

1. Add this repository to HACS as a custom repository.
2. Install the "Energy Identification" integration via HACS.
3. Add the following configuration to your `configuration.yaml`:

```yaml
sensor:
  - platform: energy_identification
    name: "Identified Appliance"
    model_path: "/config/energy_model.pkl"
    sensor: "sensor.energy_usage"
