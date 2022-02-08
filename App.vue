<template>
    <div>
        <title>
            W1MX Remote Tuner Control Panel
        </title>
        <h1>
            W1MX Remote Tuner Control Panel
        </h1>
        <p>
            This page controls the Elecraft KAT500 Antenna Tuner on the W1MX HF station in Walker Memorial (room 50-358). The tuner is capable of automatically tuning itself when you transmit, but this functionality is finicky and prone to randomly retuning while transmitting, so "manual" mode is preferred. In this mode, the tuner still chooses inductor and capacitor values automatically, but the user must manually initiate and end the tuning process.
        </p>
        <p>
            The tuner works by measuring reflected RF power, so it can <b>not</b> tune unless power is being transmitted through it. However, transmitting the full 100 W for tuning can be dangerous, so set the FlexRadio to 10-20 W for tuning, then increase power as necessary once tuning has been completed.
        </p>
        <p>
            Recommended in-person tuning procedure:
            <ol>
                <li>
                    Use the antenna switch controller connect the FlexRadio to your antenna of choice. Make sure you are seeing some reasonable received signal so that you know the antenna switch's relays actually made good contact.
                </li>
                <li>
                    Use the "PWR" knob on the FlexRadio to decrease RF transmit power to 10-20 W.
                </li>
                <li>
                    Press the "MODE" button on the tuner until the LEDs indicate that it is in "MAN" mode.
                </li>
                <li>
                    Press the "TUNE" button on the tuner. You may hear a relay click, and the "MAN" LED will start blinking. Since no power is being transmitted, the tuner cannot yet tune.
                </li>
                <li>
                    Use the frequency knob of the FlexRadio to move to an <i>empty</i> frequency on the band you wish to use. This ensures that your tuning transmissions will not interfere with other users of the band.
                </li>
                <li>
                    Press the "TUNE" button on the FlexRadio. This will cause the radio to transmit. You will start hearing many rapid relay clicks as the tuner tries different inductor/capacitor values. Wait until the clicking stops, indicating that the tuning process has completed. Once the clicking has stopped, you can press the "TUNE" button once more to stop transmitting.
                </li>
                <li>
                    Pick up the microphone and identify the station as W1MX.
                </li>
            </ol>
        </p>
        <p>
            Recommended remote tuning procedure:
            <ol>
                <li>
                    Use the antenna switch controller (<a href="http://w1mx-remote-op.mitrs.org:7010">linked here</a>) connect the FlexRadio to your antenna of choice. Make sure you are seeing some reasonable received signal so that you know the antenna switch's relays actually made good contact.
                </li>
                <li>
                    Forward packets from the FlexRadio to your local computer using the forwarding control page <a href="http://w1mx-remote-op.mitrs.org:8080">linked here</a>. Install the SmartSDR software and connect to the FlexRadio with it.
                </li>
                <li>
                    Use the "PWR" setting in SmartSDR to decrease RF transmit power to 10-20 W.
                </li>
            </ol>
        </p>
        <div id="tuner_status">
            <h2>
                KAT500 Tuner Status
            </h2>
            <p>
                Last status update to this page: {{ lastWebStatusUpdateAgo }} seconds ago
            </p>
            <p>
                Last status update received from KAT500: {{ lastHardwareStatusUpdateAgo }} seconds ago
            </p>
            <p>
                Number of users connected: {{ usersConnected }}
            </p>
            <p>
                Last user interaction: {{ userInteractionAgo }} seconds ago
            </p>
            <hline>
            <p>
                KAT500 firmware revision: {{ firmwareRevision }}
            </p>
            <p>
                KAT500 powered: {{ powered }}
            </p>
            <p>
                Last measured VSWR: {{ vswr }}
                <br>
                <i>Note that VSWR is only measured while transmitting.</i>
            </p>
            <p>
                Mode:
                <br>
                <input type="radio" name="mode" value="bypass" v-model="mode"> Bypass
                <br>
                <input type="radio" name="mode" value="manual" v-model="mode"> Manual
                <br>
                <input type="radio" name="mode" value="auto" v-model="mode"> Auto
            </p>
            <p>
                Fault: {{ faultName }} (fault code {{ faultCode }}) &mdash; {{ faultDescription }}
            </p>
            <p>
                Last frequency counter measurement: {{ frequencyCounter }} kHz
                <br>
                <i>Note that frequency is only measured while transmitting.</i>
            </p>
            <button @click="handleTuneButton">
                Tune
            </button>
        </div>
    </div>
</template>

<style>
    body {
        background-color: black;
        color: white;
        font-family: Verdana;
    }

    #tuner_status {
        border: 3px solid white;
        border-radius: 10px;
        padding-top: 10px;
        padding-bottom: 10px;
        padding-left: 20px;
        padding-right: 20px;
    }

    button {
        padding-top: 5px;
        padding-bottom: 5px;
        padding-left: 10px;
        padding-right: 10px;
        background-color: green;
        color: white;
        border: 3px solid white;
        border-radius: 10px;
    }
</style>

<script>
export default {
    mounted() {
        const url = new URL("/api", window.location.href);
        url.port = 7030;
        url.protocol = url.protocol.replace("https", "wss");
        url.protocol = url.protocol.replace("http", "ws");
        this.socket = new WebSocket(url.href);
        this.socket.addEventListener("message", this.handleSocketMessage);
    },
    unmounted() {
        this.socket.removeEventListener("message", this.handleSocketMessage);
    },
    data() {
        return {
            socket: null,
            lastWebStatusUpdateAgo: "???",
            lastHardwareStatusUpdateAgo: "???",
            usersConnected: "???",
            userInteractionAgo: "???",
            firmwareRevision: "???",
            powered: "???",
            vswr: "???",
            mode: "???",
            faultName: "???",
            faultCode: "???",
            faultDescription: "???",
            frequencyCounter: "???",
        };
    },
    methods: {
        handleSocketMessage(event) {
            console.log(event.data);
        },
        handleTuneButton() {

        },
    },
}
</script>
