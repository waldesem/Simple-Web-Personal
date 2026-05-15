<script setup lang="ts">
import { computed, PropType } from "vue";
import { fallbackParser, schemaDoc } from "@/schema";
import type { FormField, Passport } from "@/types";

const emit = defineEmits(["update"]);

const props = defineProps({
  item: {
    type: Object as PropType<Passport>,
    default: () => ({}),
  },
  fields: {
    type: Array as PropType<FormField[]>,
    required: true,
  },
});

const fallback = computed(() => fallbackParser(schemaDoc, props.item));
</script>

<template>
  <FormCard
    :fields="props.fields"
    :item="fallback"
    :schema="schemaDoc"
    @submit="emit('update', $event)"
  />
</template>
