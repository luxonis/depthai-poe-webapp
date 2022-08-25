<template>
  <div>
    <navbar></navbar>
    <div class="d-flex">
      <sidebar></sidebar>
      <div class="content p-4">
        <h2 class="mb-4">Home</h2>
        <div class="row mb-4">

          <div class="col-md">
            <div class="d-flex border">
              <div class="bg-info text-light p-4">
                <div class="d-flex align-items-center h-100">
                  <i class="fa fa-3x fa-fw fa-id-badge"></i>
                </div>
              </div>
              <div class="flex-grow-1 bg-white p-4">
                <p class="text-uppercase text-secondary mb-0">Device ID</p>
                <h3 class="font-weight-bold mb-0">{{ deviceId }}</h3>
              </div>
            </div>
          </div>

         <div class="col-md">
            <div class="d-flex border">
              <div class="bg-info text-light p-4">
                <div class="d-flex align-items-center h-100">
                  <i class="fa fa-3x fa-fw fa-code-branch"></i>
                </div>
              </div>
              <div class="flex-grow-1 bg-white p-4">
                <p class="text-uppercase text-secondary mb-0">FW Version</p>
                <h3 class="font-weight-bold mb-0">{{ fwVersion }}</h3>
              </div>
            </div>
          </div>

        </div>

        <h2 class="mb-4">Stats</h2>
        <div class="row mb-4">

          <div class="col-md">
            <div class="d-flex border">
              <div class="bg-primary text-light p-4">
                <div class="d-flex align-items-center h-100">
                  <i class="fa fa-3x fa-fw fa-cog"></i>
                </div>
              </div>
              <div class="flex-grow-1 bg-white p-4">
                <p class="text-uppercase text-secondary mb-0">CPU 1 (CSS) Usage</p>
                <h3 class="font-weight-bold mb-0">{{ cpuCssUsage }}%</h3>
              </div>
            </div>
          </div>

          <div class="col-md">
            <div class="d-flex border">
              <div class="bg-primary text-light p-4">
                <div class="d-flex align-items-center h-100">
                  <i class="fa fa-3x fa-fw fa-cog"></i>
                </div>
              </div>
              <div class="flex-grow-1 bg-white p-4">
                <p class="text-uppercase text-secondary mb-0">CPU 2 (MSS) Usage</p>
                <h3 class="font-weight-bold mb-0">{{ cpuMssUsage }}%</h3>
              </div>
            </div>
          </div>

          <div class="col-md">
            <div class="d-flex border">
              <div class="bg-dark text-light p-4">
                <div class="d-flex align-items-center h-100">
                  <i class="fa fa-3x fa-fw fa-memory"></i>
                </div>
              </div>
              <div class="flex-grow-1 bg-white p-4">
                <p class="text-uppercase text-secondary mb-0">CPU 1 (CSS) Memory</p>
                <h3 class="font-weight-bold mb-0">{{ memCssUsage }}/{{ memCssTotal }} MiB</h3>
              </div>
            </div>
          </div>

          <div class="col-md">
            <div class="d-flex border">
              <div class="bg-dark text-light p-4">
                <div class="d-flex align-items-center h-100">
                  <i class="fa fa-3x fa-fw fa-memory"></i>
                </div>
              </div>
              <div class="flex-grow-1 bg-white p-4">
                <p class="text-uppercase text-secondary mb-0">CPU 2 (MSS) Memory</p>
                <h3 class="font-weight-bold mb-0">{{ memMssUsage }}/{{ memMssTotal }} MiB</h3>
              </div>
            </div>
          </div>

          <div class="col-md">
            <div class="d-flex border">
              <div class="bg-success text-light p-4">
                <div class="d-flex align-items-center h-100">
                  <i class="fa fa-3x fa-fw fa-thermometer-three-quarters"></i>
                </div>
              </div>
              <div class="flex-grow-1 bg-white p-4">
                <p class="text-uppercase text-secondary mb-0">Temperature</p>
                <h3 class="font-weight-bold mb-0">{{ tempAverage }}*C</h3>
              </div>
            </div>
          </div>

        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Navbar from "../components/Navbar"
import Sidebar from "../components/Sidebar"
export default {
  components: { Sidebar, Navbar },
  data() {
    return {
      cpuCssUsage: 10,
      cpuMssUsage: 10,
      memCssUsage: 2,
      memCssTotal: 50,
      memMssUsage: 20,
      memMssTotal: 70,
      tempAverage: 77,
      alive: true,
      fwVersion: '2d804ddd22b8f22f4067ce22772c930417aec6c1',
      deviceId: '144477AB353FD700'
    }
  },
  mounted () {
    document.title = "DepthAI PoE WebApp"
    console.log('Index mounted');
    this.fetchStats();
    this.alive = true;
    this.fetchFwVersion();
    this.fetchDeviceId();
  },
  beforeDestroy(){
    console.log('Index beforeDestroy');
    this.alive = false;
  },
  methods: {
    fetchStats(){
      this.axios
        .get('/api/stats')
        .then(response => {
          let d = response.data;
          this.cpuCssUsage = (d["cpu_css_percent"] * 100).toFixed(2);
          this.cpuMssUsage = (d["cpu_mss_percent"] * 100).toFixed(2);

          this.memCssUsage = (d["mem_css_used"] / 1024 / 1024).toFixed(1);
          this.memCssTotal = (d["mem_css_total"] / 1024 / 1024).toFixed(1);
          this.memMssUsage = (d["mem_mss_used"] / 1024 / 1024).toFixed(1);
          this.memMssTotal = (d["mem_mss_total"] / 1024 / 1024).toFixed(1);

          this.tempAverage = (d["temp_average"]).toFixed(1);
          // update again after 1s
          if(this.alive) {
            setTimeout(this.fetchStats, 1000);
          }
        })
        .catch(error => {
          console.log(error)
          // update again after 1s
          if(this.alive) {
            setTimeout(this.fetchStats, 1000);
          }
        })
    },
    fetchFwVersion(){
      this.axios
        .get('/api/fw_version')
        .then(response => {
          let d = response.data;
          this.fwVersion = d['fw_version'];
        })
    },
    fetchDeviceId(){
      this.axios
        .get('/api/device_id')
        .then(response => {
          let d = response.data;
          this.deviceId = d['device_id'];
        })
    }
  }
}
</script>
