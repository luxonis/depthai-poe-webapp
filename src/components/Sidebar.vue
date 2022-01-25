<template>
  <div>
    <div :class="{'toggled': $root.showSidebar}" class="sidebar sidebar-dark bg-dark">
      <ul class="list-unstyled">
        <li>
          <router-link class="nav-link" to="/"><i class="icon fa fa-home"></i> Home</router-link>
        </li>
        <li>
          <router-link class="nav-link" to="/cameras"><i class="icon fa fa-camera"></i> Cameras</router-link>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  mounted () {}
}
</script>
