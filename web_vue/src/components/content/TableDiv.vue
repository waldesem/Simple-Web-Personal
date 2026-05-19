<script setup lang="ts">
import type { PropType } from "vue";
import type { TableColumns } from "@/types";

const emit = defineEmits(["select"]);

const props = defineProps({
  cols: {
    type: Array as PropType<TableColumns<any>[]>,
    required: true,
  },
  data: {
    type: Array as PropType<Record<string, any>[]>,
    required: true,
  },
});
</script>

<template>
  <div class="relative overflow-auto">
    <table class="table-fixed min-w-full overflow-clip">
      <thead class="relative">
        <tr>
          <th
            v-for="(row, index) in props.cols"
            :key="index"
            class="p-4 text-sm text-highlighted text-left"
          >
            {{ row.header }}
          </th>
        </tr>
      </thead>
      <tbody class="isolate divide-y divide-default">
        <tr
          v-for="(item, index) in props.data"
          :key="index"
          class="hover:bg-gray-100 cursor-pointer"
          @click="emit('select', item.id)"
        >
          <td
            v-for="(row, idx) in props.cols"
            :key="idx"
            class="p-4 text-sm text-muted whitespace-nowrap"
          >
            {{ row.cell ? row.cell(item) : item[row.name as keyof typeof row] }}
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
