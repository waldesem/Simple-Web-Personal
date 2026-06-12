<script setup lang="ts">
import { shallowRef, type PropType } from "vue";
import type { ItemFields } from "@/types";

const emits = defineEmits(["update", "delete"]);

const visible = shallowRef(false);

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
    <Transition name="fade">
      <div v-show="visible" class="relative">
        <UFieldGroup class="absolute right-1" size="sm">
          <UButton
            color="neutral"
            icon="i-mi-edit-alt"
            title="Изменить"
            variant="outline"
            @click="emits('update')"
          />
          <UButton
            color="neutral"
            icon="i-mi-delete"
            title="Удалить"
            variant="outline"
            @click="emits('delete')"
          />
        </UFieldGroup>
      </div>
    </Transition>

    <div v-for="field in fields" :key="field.key" class="m-2">
      <div
        v-if="
          (item[field.key] !== '' && item[field.key] !== null) || field.slot
        "
        class="flex grid grid-cols-12 gap-3 mb-4"
      >
        <div class="col-span-3">{{ field.label }}</div>
        <div class="col-span-9 wrap-break-word">
          <component v-if="field.component" :is="field.component(item)" />
          <slot v-else-if="field.slot" :name="field.key" />
          <span v-else>
            {{ field.div ? field.div(item) : item[field.key] }}
          </span>
        </div>
      </div>
    </div>
    <slot></slot>
  </div>
</template>
