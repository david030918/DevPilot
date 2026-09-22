import {z} from "zod";
import {useForm} from "react-hook-form";
import {zodResolver} from "@hookform/resolvers/zod";
import {useMutation, useQueryClient} from "@tanstack/react-query";
import {ApiError, createProject} from "../api";

export default function CreateProjectForm() {
    const createProjectSchema = z.object({
        name: z.string().min(1, "Name is required"),
        repositoryOwner: z.string().min(1, "Repository owner is required"),
        repositoryName: z.string().min(1, "Repository name is required"),
        defaultBranch: z.string().min(1, "Default branch is required"),
    });

    type CreateProjectFormValues = z.infer<typeof createProjectSchema>;

    const {
        register,
        handleSubmit,
        formState: {errors},
    } = useForm<CreateProjectFormValues>({
        resolver: zodResolver(createProjectSchema),
        defaultValues: {
            defaultBranch: "main",
        },
    });

    const queryClient = useQueryClient();
    const createProjectMutation = useMutation({
            mutationFn: createProject,
            onSuccess: () => {
                queryClient.invalidateQueries({queryKey: ["projects"]})
            },
        },
    )

    return (
        <form onSubmit={handleSubmit((data) => createProjectMutation.mutate(data))}>
            {createProjectMutation.error && (
                <p role="alert">
                    {createProjectMutation.error instanceof ApiError && (
                        createProjectMutation.error.status === 409
                            ? "Project already exists"
                            : createProjectMutation.error.status === 400
                                ? "backend validation"
                                : "Unable to create project")}
                </p>
            )}
            <label>
                Name
                {errors.name && <span>{errors.name.message}</span>}
                <input {...register("name")}/>
            </label>
            <label>
                Repository Owner
                {errors.repositoryOwner && <span>{errors.repositoryOwner.message}</span>}
                <input {...register("repositoryOwner")} />
            </label>
            <label>
                Repository Name
                {errors.repositoryName && <span>{errors.repositoryName.message}</span>}
                <input {...register("repositoryName")} />
            </label>
            <label>
                Default Branch
                {errors.defaultBranch && <span>{errors.defaultBranch.message}</span>}
                <input {...register("defaultBranch")} />
            </label>
            <button type="submit" disabled={createProjectMutation.isPending}>
                {createProjectMutation.isPending ? "Creating Project..." : "Create Project"}
            </button>
        </form>
    );
}
