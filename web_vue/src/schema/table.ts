import { localStr, timeAgoStr } from "@/utils";
import type { Person, TableColumns } from "@/types";

export const tableColumns: TableColumns<Person>[] = [
  {
    name: "id",
    header: "#",
  },
  {
    name: "surname",
    header: "Фамилия",
  },
  {
    name: "firstname",
    header: "Имя",
  },
  {
    name: "patronymic",
    header: "Отчество",
  },
  {
    name: "birthday",
    header: "Дата рождения",
    cell: (row) => {
      return localStr(row.birthday);
    },
  },
  {
    name: "created",
    header: "Обновлено",
    cell: (row) => {
      return timeAgoStr(row.created);
    },
  },
];