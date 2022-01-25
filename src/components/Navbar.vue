<template>
  <div>
    <nav class="navbar navbar-expand navbar-dark bg-primary">
      <a style="margin-left: -10px" class="btn btn-link text-white mr-2" href="#" @click.prevent="$root.showSidebar = !$root.showSidebar">
        <i class="fas fa-bars"></i>
      </a>
      <router-link class="navbar-brand" to="/">
        <img alt="Icon" class="navbar-icon d-inline-block align-top" src="../assets/images/depthai_logo.png">
        <span class="navbar-title">DepthAI</span>
      </router-link>
    </nav>
  </div>
</template>

<script>
export default {
  mounted () {}
}
</script>
