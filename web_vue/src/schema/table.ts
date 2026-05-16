import type { Person, TableColumns } from "@/types";
import { localStr, timeAgoStr } from "@/utils";

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
    cell: (row) => localStr(row.birthday),
  },
  {
    name: "created",
    header: "Обновлено",
    cell: (row) => timeAgoStr(row.created),
  },
];
