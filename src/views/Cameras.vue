<template>
  <div>
    <navbar></navbar>
    <div class="d-flex">
      <sidebar></sidebar>
      <div class="content p-4">
        <h2 class="mb-4">Cameras</h2>

        <!-- Left & Right streams in its own row -->
        <!-- check if left/right are available -->
        <div class="row mb-4">

          <div class="col-md">
            <img ref="camera_stream_left" src="" class="img-fluid" />
          </div>
          <div class="col-md">
            <img ref="camera_stream_right" src="" class="img-fluid" />
          </div>

        </div>

        <!-- Color stream in its own row -->
        <div class="row mb-4">
          <div class="col-md">
            <img ref="camera_stream_color" src="" class="img-fluid" />
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script>
import jQuery from "jquery"
import Navbar from "../components/Navbar"
import Sidebar from "../components/Sidebar"

export default {
  components: { Sidebar, Navbar },
  mounted () {
    document.title = "DepthAI - Cameras"
    let $ = jQuery
    $(".select2").select2({
      width: "100%"
    })
    console.log('Starting camera streams');
    this.$refs.camera_stream_left.setAttribute('src', '/stream/left')
    this.$refs.camera_stream_right.setAttribute('src', '/stream/right')
    this.$refs.camera_stream_color.setAttribute('src', '/stream/color')
  },
  beforeDestroy() {
    console.log('Stopping camera streams')
    this.$refs.camera_stream_left.setAttribute('src', '')
    this.$refs.camera_stream_right.setAttribute('src', '')
    this.$refs.camera_stream_color.setAttribute('src', '')
  },
}
</script>
