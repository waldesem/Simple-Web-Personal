<script setup lang="ts">
import { ref, type PropType } from "vue";
import { Roles, type ItemFields } from "@/types";
import { session } from "@/state";

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

const buttons = [
  { icon: "i-mi-edit-alt", title: "Изменить", emit: "update" },
  { icon: "i-mi-delete", title: "Удалить", emit: "delete" },
] as { icon: string; title: string; emit: Parameters<typeof emits>[0] }[];
</script>

<template>
  <div @mouseover="visible = true" @mouseleave="visible = false">
    <Transition name="fade">
      <div v-show="visible && session.role === Roles.admin" class="relative">
        <UFieldGroup class="absolute right-1" size="sm">
          <UButton
            v-for="(button, index) in buttons"
            :key="index"
            :icon="button.icon"
            :title="button.title"
            color="neutral"
            variant="outline"
            @click="emits(button.emit)"
          />
        </UFieldGroup>
      </div>
    </Transition>

    <div v-for="field in props.fields" :key="field.key" class="m-2">
      <div
        v-if="
          (item[field.key] !== '' && item[field.key] !== null) || field.slot
        "
        class="grid grid-cols-12 gap-3 mb-4"
      >
        <div class="col-span-3">{{ field.label }}</div>
        <div class="col-span-9 wrap-break-word">
          <component v-if="field.component" :is="field.component(item)" />
          <slot v-else-if="field.slot" :name="field.key" />
          <span v-else>
            {{ field.foo ? field.foo(item) : item[field.key] }}
          </span>
        </div>
      </div>
    </div>
    <slot></slot>
  </div>
</template>
