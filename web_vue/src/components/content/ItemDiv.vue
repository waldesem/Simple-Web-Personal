<script setup lang="ts">
import { ref, type PropType } from "vue";
import type { ItemFields } from "@/types";

const emits = defineEmits(["update", "delete"]);

const visible = ref(false);

const props = defineProps({
  fields: {
    type: Array as PropType<ItemFields<any>[]>,
    required: true,
  },
  item: {
    type: Object as PropType<any>,
    default: () => ({}),
  },
});
</script>

<template>
  <div @mouseover="visible = true" @mouseleave="visible = false">
    <div v-show="visible" class="relative">
      <NUFieldGroup class="absolute right-1" size="sm">
        <NUButton
          color="neutral"
          icon="i-mi-edit-alt"
          title="Изменить"
          variant="outline"
          @click="emits('update')"
        />
        <NUButton
          color="neutral"
          icon="i-mi-delete"
          title="Удалить"
          variant="outline"
          @click="emits('delete')"
        />
      </NUFieldGroup>
    </div>

    <div v-for="field in fields" :key="field.key" class="m-2">
      <div
        v-if="typeof item[field.key] !== 'object'"
        class="flex grid grid-cols-12 gap-3 mb-4"
      >
        <div class="col-span-3">
          {{ field.label }}
        </div>
        <div class="col-span-9 wrap-break-word">
          <component v-if="field.component" :is="field.component(item)" />
          <slot v-else-if="field.slot" :name="field.key" />
          <span v-else>{{
            field.div ? field.div(item) : item[field.key]
          }}</span>
        </div>
      </div>
    </div>
    <slot></slot>
  </div>
</template>
