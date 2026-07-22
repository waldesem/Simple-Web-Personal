<script setup lang="ts">
import { ref, type PropType } from "vue";
import { session } from "@/state";
import type { person as PersonField, itemsFields } from "@/schema/items";
import { Items, Person, Roles } from "@/types";
import ItemRow from "./ItemRow.vue";

const emits = defineEmits(["update", "delete"]);

const visible = ref(false);

const props = defineProps({
  fields: {
    type: Array as PropType<
      typeof PersonField | (typeof itemsFields)[keyof typeof itemsFields]
    >,
    required: true,
  },
  item: {
    type: Object as PropType<Person | Items[keyof Items]>,
    default: () => ({}),
  },
});
</script>

<template>
  <div @mouseover="visible = true" @mouseleave="visible = false">
    <Transition name="fade">
      <div v-show="visible && session.role === Roles.user" class="relative">
        <UFieldGroup class="absolute right-0" size="sm">
          <UButton
            icon="i-lucide-square-pen"
            title="Изменить"
            color="neutral"
            variant="outline"
            @click="emits('update')"
          />
          <UButton
            icon="i-lucide-trash"
            title="Удалить"
            color="neutral"
            variant="outline"
            @click="emits('delete')"
          />
        </UFieldGroup>
      </div>
    </Transition>

    <template v-for="field in props.fields" :key="field.key">
      <ItemRow
        v-if="
          (item[field.key as keyof typeof item] !== '' &&
            item[field.key as keyof typeof item] !== null) ||
          field.slot
        "
        :data="item"
        :field="field"
      />
    </template>
    <slot></slot>
  </div>
</template>
