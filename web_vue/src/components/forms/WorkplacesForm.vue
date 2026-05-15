<script setup lang="ts">
import { computed, PropType } from "vue";
import { fallbackParser, schemaWork } from "@/schema";
import type { FormField, Work } from "@/types";

const emit = defineEmits(["update"]);

const props = defineProps({
  item: {
    type: Object as PropType<Work>,
    default: () => ({}),
  },
  fields: {
    type: Array as PropType<FormField[]>,
    required: true,
  },
});

const fallback = computed(() => fallbackParser(schemaWork, props.item));
</script>

<template>
  <FormCard
    :fields="props.fields"
    :item="fallback"
    :schema="schemaWork"
    @submit="emit('update', $event)"
  />
</template>
