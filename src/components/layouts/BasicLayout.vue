<template>
    <div class="basic-layout flex flex-row">
        <div class="side-bar">
            <div class="user-info">
                <slot name="user-info">User1</slot>
            </div>
            <div class="notification">
                <slot name="notification">Notification1</slot>
            </div>
        </div>
        <div class="main-content">
            <slot name="main-content">Content1</slot>
        </div>
    </div>
</template>

<style scoped>
.basic-layout {
  display: flex;
  height: 100vh;
  width: 100vw;
  flex-direction: row;
  justify-content: start;
  padding: 0;
  margin: 0;
}

.side-bar {
  width: 300px;
  height: 100vh;
  background-color: #f0f0f0;
  display: flex;
  flex-direction: column;
  justify-content: start;
  align-items: center;
  margin: 0;
  padding: 0;
}

.user-info {
  height: 120px;
  width: 100%;
  background-color: #f0f0f0;
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 0;
  padding: 0;
}
.notification {
  height: calc(100vh - 120px);
  width: 100%;
  background-color: #e0e0e0;
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 0;
  padding: 0;
}
.main-content {
  flex: 1;
  background-color: #ffffff;
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 0;
  padding: 0;
}

</style>
