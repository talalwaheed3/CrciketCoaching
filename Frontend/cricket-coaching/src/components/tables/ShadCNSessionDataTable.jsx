// import { useContext, useEffect, useState } from "react";
// import {
//   useReactTable,
//   getCoreRowModel,
//   flexRender,
// } from "@tanstack/react-table";
// import {
//   Table,
//   TableHeader,
//   TableRow,
//   TableHead,
//   TableBody,
//   TableCell,
// } from "@/components/ui/table";
// import handleRequest from "../../utils/handleRequest";
// import AuthContext from "../auth/AuthContext";

// const columns = [
//   { accessorKey: "id", header: "ID" },
//   { accessorKey: "name", header: "Session Name" },
//   { accessorKey: "player", header: "Player Name" },
//   { accessorKey: "date", header: "Date" },
//   { accessorKey: "from", header: "Session From" },
//   { accessorKey: "to", header: "Session To" },
//   { accessorKey: "venue", header: "Venue" },
// ];

// const DataTable = ({ endpoint }) => {
//   const { user } = useContext(AuthContext);
//   const [tableData, setTableData] = useState([]);

//   const table = useReactTable({
//     data: tableData,
//     columns,
//     getCoreRowModel: getCoreRowModel(),
//   });

//   const handleDisplayData = async () => {
//     try {
//       const repsonse = await handleRequest(endpoint, "POST", {
//         coach_id: user.id,
//       });
//       console.log("response from handle handleRequest is:", repsonse);
//       setTableData(repsonse);
//     } catch (error) {
//       alert("error is while fetching response is:", error);
//       console.error("error is while fetching response is:", error);
//     }
//   };

//   useEffect(() => {
//     handleDisplayData();
//   }, []);

//   return (
//     <div className="p-4 border rounded-lg shadow-md relative top-60">
//       <Table className="h-[150px]">
//         <TableHeader className="bg-gray-200">
//           {table.getHeaderGroups().map((headerGroup) => (
//             <TableRow key={headerGroup.id} className="border-b">
//               {headerGroup.headers.map((header) => (
//                 <TableHead key={header.id} className="text-center px-4 py-2">
//                   {flexRender(
//                     header.column.columnDef.header,
//                     header.getContext()
//                   )}
//                 </TableHead>
//               ))}
//             </TableRow>
//           ))}
//         </TableHeader>
//         <TableBody>
//           {table.getRowModel().rows.length ? (
//             table.getRowModel().rows.map((row) => (
//               <TableRow key={row.id} className="hover:bg-gray-100">
//                 {row.getVisibleCells().map((cell) => (
//                   <TableCell key={cell.id} className="px-4 py-2 text-center">
//                     {flexRender(cell.column.columnDef.cell, cell.getContext())}
//                   </TableCell>
//                 ))}
//               </TableRow>
//             ))
//           ) : (
//             <TableRow>
//               <TableCell colSpan={columns.length} className="text-center py-4">
//                 No data available
//               </TableCell>
//             </TableRow>
//           )}
//         </TableBody>
//       </Table>
//     </div>
//   );
// };

// export default DataTable;
