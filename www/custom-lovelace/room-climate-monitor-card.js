class RoomClimateMonitorCard extends HTMLElement {
  setConfig(config) {
    this.config = config;
  }

  connectedCallback() {
    this.innerHTML = `
      <ha-card>
        <h1>Room Climate Monitor</h1>
        <div>Temperature: ${this.config.temperature} °C</div>
        <div>Humidity: ${this.config.humidity} %</div>
        <div>Status: ${this.config.status}</div>
      </ha-card>
    `;
  }
}

customElements.define('room-climate-monitor-card', RoomClimateMonitorCard);
