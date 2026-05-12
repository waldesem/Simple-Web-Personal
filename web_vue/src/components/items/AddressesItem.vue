<script setup lang="ts">
import { PropType } from "vue";
import type { Address, ItemField } from "@/types";

const props = defineProps({
  item: {
    type: Object as PropType<Address>,
    required: true,
  },
});

const fields = [
  { key: "view", label: "Тип", value: props.item.view },
  { key: "address", label: "Адрес", value: props.item.address },
] as ItemField[];
</script>

<template>
  <ItemCard :fields="fields" />
</template>
