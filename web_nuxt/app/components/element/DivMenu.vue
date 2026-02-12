<script setup lang="ts">
// Компонент для отображения выпадающего списка действий
const emits = defineEmits(["update", "delete"]);
</script>

<template>
  <div class="relative">
    <div class="absolute right-0">
      <UDropdownMenu
        :items="[
          {
            label: 'Изменить',
            onSelect() {
              emits('update');
            },
          },
          {
            label: 'Удалить',
            onSelect() {
              emits('delete');
            },
          },
        ]"
        :content="{ align: 'end' }"
      >
        <UButton
          color="neutral"
          icon="i-lucide-ellipsis-vertical"
          variant="ghost"
          title="Выбор действия"
        />
      </UDropdownMenu>
    </div>
  </div>
</template>
