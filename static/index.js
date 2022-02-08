Vue.createApp({
    mounted() {
        const url = new URL("/api", window.location.href);
        url.protocol = url.protocol.replace("https", "wss");
        url.protocol = url.protocol.replace("http", "ws");
        this.socket = new WebSocket(url.href);
        this.socket.addEventListener("message", this.handleSocketMessage);
    },
    unmounted() {
        this.socket.removeEventListener("message", this.handleSocketMessage);
    },
    data: () => {
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
    },
}).mount("#vue_div");
