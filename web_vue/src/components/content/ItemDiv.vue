<script lang="ts">
import type { PropType } from 'vue';
import type {
  person as PersonFieldsType,
  itemsFields as ItemsFieldsType,
} from '@/schema/items';

export type ItemType = Person | Items[keyof Items];

export type FieldsType =
  | typeof PersonFieldsType
  | (typeof ItemsFieldsType)[keyof typeof ItemsFieldsType];
</script>

<script setup lang="ts">
import { ref } from 'vue';
import { session } from '@/state';
import { Items, Person, Roles } from '@/types';
import ItemRow from './ItemRow.vue';

const emits = defineEmits(['update', 'delete']);

const visible = ref(false);

const { fields, item } = defineProps({
  fields: {
    type: Array as PropType<FieldsType>,
    required: true,
  },
  item: {
    type: Object as PropType<ItemType>,
    required: true,
  },
});
</script>

<template>
  <div @mouseover="visible = true" @mouseleave="visible = false">
    <Transition name="fade">
      <div
        v-show="visible && session.role === Roles.user"
        class="relative no-print"
      >
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

    <template v-for="field in fields" :key="field.key">
      <ItemRow v-if="field.slot" :data="item" :field="field">
        <slot :name="field.key"></slot>
      </ItemRow>
      <ItemRow
        v-else-if="item[field.key as keyof typeof item]"
        :data="item"
        :field="field"
      />
    </template>
  </div>
</template>
