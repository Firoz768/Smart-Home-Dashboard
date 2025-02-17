import streamlit as st
from data.mock_data import rooms, devices
from utils.state_management import init_state, toggle_theme
from utils.theme import apply_theme
from components.room_section import render_room_section
from iot.device_manager import get_device_manager
from config.iot_config import MQTT_BROKER, MQTT_PORT

# Initialize the app state
init_state()

# Apply theme
apply_theme()

# App header
st.title("🏠 Smart Home Dashboard")

# Settings sidebar
with st.sidebar:
    st.title("Settings")
    st.button("🌓 Toggle Theme", on_click=toggle_theme)

    # IoT Connection Settings
    st.markdown("### 🔌 IoT Device Connection")
    broker = st.text_input("MQTT Broker", value=MQTT_BROKER)
    port = st.number_input("MQTT Port", value=MQTT_PORT, min_value=1, max_value=65535)

    if st.button("Connect to IoT Network"):
        try:
            device_manager = get_device_manager()
            device_manager.connect(broker, port)
            st.success("Successfully connected to IoT network!")
            st.session_state.iot_connected = True
        except Exception as e:
            st.error(f"Failed to connect: {str(e)}")
            st.session_state.iot_connected = False

    # Connection status indicator
    if st.session_state.get('iot_connected', False):
        st.success("🟢 Connected to IoT network")
    else:
        st.warning("🔴 Not connected to IoT network")

    # Device Discovery
    if st.session_state.get('iot_connected', False):
        st.markdown("### 🔍 Device Discovery")
        if st.button("Scan for Devices"):
            device_manager = get_device_manager()
            try:
                discovered_devices = device_manager.discover_devices()
                st.session_state.discovered_devices = discovered_devices
                st.success(f"Found {len(discovered_devices)} devices!")
            except Exception as e:
                st.error(f"Error scanning for devices: {str(e)}")

    # Notification settings
    st.markdown("### 📱 Notifications")
    if 'notification_phone' not in st.session_state:
        st.session_state.notification_phone = ""

    notification_phone = st.text_input(
        "Phone Number for Notifications",
        value=st.session_state.notification_phone,
        help="Enter your phone number to receive device status notifications",
        placeholder="+1234567890"
    )
    if notification_phone != st.session_state.notification_phone:
        st.session_state.notification_phone = notification_phone

# Display stats
st.markdown("### Quick Stats")
stat1, stat2, stat3, stat4 = st.columns(4)
with stat1:
    st.metric("Temperature", "22°C", "+1°C")
with stat2:
    st.metric("Humidity", "45%", "-2%")
with stat3:
    st.metric("Energy Usage", "3.2kW", "-0.4kW")
with stat4:
    st.metric("Active Devices", "8", "+2")

# Render rooms and their devices
for room_name, room_image in rooms.items():
    st.markdown("---")
    render_room_section(room_name, devices[room_name], room_image)

# Footer
st.markdown("---")
st.markdown("### Automation Rules")
with st.expander("View Active Rules"):
    st.write("1. Turn off all lights when nobody is home")
    st.write("2. Set temperature to 20°C at night")
    st.write("3. Turn on coffee maker at 7 AM on weekdays")

# Add some spacing at the bottom
st.markdown("<br><br>", unsafe_allow_html=True)