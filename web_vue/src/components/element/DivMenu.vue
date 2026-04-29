<script setup lang="ts">
const emits = defineEmits(["update", "delete"]);
</script>

<template>
  <div v-once class="relative">
    <div class="absolute right-0">
      <UDropdownMenu
        :items="[
          {
            label: 'Изменить',
            icon: 'i-lucide-square-pen',
            onSelect() {
              emits('update');
            },
          },
          {
            label: 'Удалить',
            icon: 'i-lucide-trash',
            onSelect() {
              emits('delete');
            },
          },
        ]"
        :content="{ align: 'end' }"
      >
        <UButton
          color="neutral"
          variant="ghost"
          title="Выбор действия"
          icon="i-lucide-ellipsis-vertical"
        />
      </UDropdownMenu>
    </div>
  </div>
</template>
